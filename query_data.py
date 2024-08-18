from app import app, db, Task, User, Comment

with app.app_context():
    tasks = Task.query.all()
    for task in tasks:
        print(task.title, task.category, task.description, task.reward)

    users = User.query.all()
    for user in users:
        print(user.username, user.email, user.comments)

    comments = Comment.query.all()
    for comment in comments:
        print(comment.content, comment.rating, comment.task_id, comment.user_id)