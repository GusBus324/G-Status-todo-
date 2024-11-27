from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, Date
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
    category = Column(String)  # Add this line
    due_date = Column(Date)  # Add this line
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='todos')

def init_db():
    engine = create_engine('sqlite:///todo.db')
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
