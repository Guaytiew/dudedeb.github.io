from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/dummy/Serve_Dude/database/servedude.db' # 'sqlite:///database/servedude.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the database
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to the login page if not authenticated

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reward = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='task', lazy=True)

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Setup Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    categories = Task.query.with_entities(Task.category).distinct().all()
    return render_template('index.html', categories=categories) # render_template() -> This function is used to render HTML templates. Flask looks for the templates in the templates directory by default.

@app.route('/tasks/<category>')
def tasks(category):
    tasks = Task.query.filter_by(category=category).all()
    return render_template('tasks.html', tasks=tasks, category=category)

@app.route('/task/<int:id>')
def task_detail(id):
    task = Task.query.get_or_404(id)
    sort = request.args.get('sort', 'latest')  # Default to 'latest'

    if sort == 'latest':
        comments = Comment.query.filter_by(task_id=id).order_by(Comment.id.desc()).all()
    elif sort == 'popular':
        comments = Comment.query.filter_by(task_id=id).order_by(Comment.rating.desc()).all()

    return render_template('task_detail.html', task=task, comments=comments)


@app.route('/add_comment/<int:task_id>', methods=['POST'])
@login_required  # Ensure the user is logged in
def add_comment(task_id):
    content = request.form['content']
    rating = request.form['rating']
    user_id = current_user.id  # Use the current logged-in user's ID
    new_comment = Comment(content=content, rating=rating, task_id=task_id, user_id=user_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('task_detail', id=task_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
