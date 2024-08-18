from app import app, db, Task, User, Comment

with app.app_context():

    # db.session.query(Task).delete()
    # # db.engine.execute('TRUNCATE TABLE task')
    # db.session.commit()

    
    ## delete all records from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f"Clearing table {table}")
        db.session.execute(table.delete())
    db.session.commit()

    ## drop all table
    #  db.drop_all()

    print("All records from db have been deleted.")
