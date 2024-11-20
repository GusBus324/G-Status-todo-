from sqlalchemy import create_engine, Column, Integer, String, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

#  Base class for ORM
Base = declarative_base()


# User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    

#toDo model
class ToDo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<ToDo {self.title}>'
    
# Database setup
engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
print('Database setup complete')