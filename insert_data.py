from app import app, db, Task, User, Comment

# Create the database tables if they don't exist yet
with app.app_context():
    db.create_all()

    # Insert sample users ----------------------------------------------------------------
    sample_users = [
        {"username": "JohnDoe", "email": "john@example.com"},
        {"username": "JaneDoe", "email": "jane@example.com"},
    ]

    for user_data in sample_users:
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if not existing_user:
            user = User(username=user_data["username"], email=user_data["email"])
            db.session.add(user)
        else:
            print(f"User with email {user_data['email']} already exists.")

    db.session.commit()

    # Insert sample tasks ----------------------------------------------------------------
    sample_tasks = [
        {"title": "Chickaboom", "category": "Cleaning", "description": "Clean the TonyTony's house", "reward": "50 points"},
        {"title": "Take it all", "category": "Shopping", "description": "Buy groceries", "reward": "15 points"},
        {"title": "1412", "category": "Delivery", "description": "Deliver the package", "reward": "20 points"},
        {"title": "Just Clean It!", "category": "Cleaning", "description": "Clean the BigD's yard", "reward": "10 points"},
    ]

    for task_data in sample_tasks:
        existing_task = Task.query.filter_by(title=task_data["title"]).first()
        if not existing_task:
            task = Task(title=task_data["title"], category=task_data["category"],
                        description=task_data["description"], reward=task_data["reward"])
            db.session.add(task)
        else:
            print(f"Task with title '{task_data['title']}' already exists.")

    db.session.commit()

    # Insert sample comments ----------------------------------------------------------------
    sample_comments = [
        {"content": "Great job!", "rating": 5, "task_title": "Just Clean It!", "user_email": "john@example.com"},
        {"content": "Could be better.", "rating": 3, "task_title": "1412", "user_email": "jane@example.com"},
        {"content": "The best of shit", "rating": 1, "task_title": "Just Clean It!", "user_email": "jane@example.com"},
    ]

    for comment_data in sample_comments:
        task = Task.query.filter_by(title=comment_data["task_title"]).first()
        user = User.query.filter_by(email=comment_data["user_email"]).first()

        if task and user:
            existing_comment = Comment.query.filter_by(content=comment_data["content"], task_id=task.id, user_id=user.id).first()
            if not existing_comment:
                comment = Comment(content=comment_data["content"], rating=comment_data["rating"],
                                  task_id=task.id, user_id=user.id)
                db.session.add(comment)
            else:
                print(f"Duplicate comment '{comment_data['content']}' already exists.")
        else:
            print(f"Task '{comment_data['task_title']}' or User '{comment_data['user_email']}' does not exist.")

    db.session.commit()
    print("Sample data inserted.")
