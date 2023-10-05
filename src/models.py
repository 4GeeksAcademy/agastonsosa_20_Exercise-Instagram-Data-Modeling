import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    ID = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)

    posts = relationship('Post', back_populates='user')
    followers_from = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='user_from')
    followers_to = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='user_to')
    comments = relationship('Comment', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.ID'))
    
    user = relationship('User', back_populates='posts')
    media = relationship('Media', back_populates='post')
    comments = relationship('Comment', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    ID = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', 'audio'))
    url = Column(String)
    post_id = Column(Integer, ForeignKey('posts.ID'))

    post = relationship('Post', back_populates='media')

class Follower(Base):
    __tablename__ = 'followers'
    user_from_id = Column(Integer, ForeignKey('users.ID'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('users.ID'), primary_key=True)

    user_from = relationship('User', back_populates='followers_from')
    user_to = relationship('User', back_populates='followers_to')

class Comment(Base):
    __tablename__ = 'comments'
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String)
    author_id = Column(Integer, ForeignKey('users.ID'))
    post_id = Column(Integer, ForeignKey('posts.ID'))

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')


# Crea el motor de la base de datos
engine = create_engine('sqlite:///social_media.db')
Base.metadata.create_all(engine)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e

