# from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from werkzeug.security import generate_password_hash, check_password_hash

# # Base class for ORM models
# Base = declarative_base()

# # User model
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     todos = relationship('Todo', back_populates='user')

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password, password)

# # To-do model
# class Todo(Base):
#     __tablename__ = 'todos'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     task = Column(String, nullable=False)
#     done = Column(Boolean, nullable=False)
#     user = relationship('User', back_populates='todos')

# # Database setup
# engine = create_engine('sqlite:///todo.db')
# Base.metadata.create_all(engine)
# print('Database and tables created successfully')
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    todos = relationship('ToDo', back_populates='user')

class ToDo(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='todos')

def init_db():
    engine = create_engine('sqlite:///todo.db')
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
