from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash
from Flask_app.db_create import User, ToDo  # Ensure you import the correct models

engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine)
session = Session()

# Add users with hashed passwords
user1 = User(username='john_doe', password=generate_password_hash('securepassword123'))
user2 = User(username='jane_doe', password=generate_password_hash('mypassword456'))
user3 = User(username='alice_smith', password=generate_password_hash('alicepassword789'))

session.add_all([user1, user2, user3])
session.commit()

# Add tasks
task1 = ToDo(title='Learn Flask', description='Complete Flask tutorials', done=False, user_id=user1.id)
task2 = ToDo(title='Build a To-Do App', description='Create a to-do app using Flask', done=True, user_id=user2.id)
task3 = ToDo(title='Read SQLAlchemy Docs', description='Read the official SQLAlchemy documentation', done=False, user_id=user3.id)

session.add_all([task1, task2, task3])
session.commit()

print("Users and tasks inserted successfully.")