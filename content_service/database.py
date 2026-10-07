import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PostModel(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.String(36), primary_key=True)
    author_id = db.Column(db.String(50), nullable=False)
    clan_emoji = db.Column(db.String(10), nullable=False, index=True)  # Индекс для быстрой фильтрации из ПР2
    content = db.Column(db.Text, nullable=False)
    repost_of_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    comments = db.relationship('CommentModel', backref='post', cascade='all, delete-orphan')
    likes = db.relationship('LikeModel', backref='post', cascade='all, delete-orphan')
    bookmarks = db.relationship('BookmarkModel', backref='post', cascade='all, delete-orphan')

class CommentModel(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.String(36), primary_key=True)
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class LikeModel(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.String(36), primary_key=True)
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    clan_emoji = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class BookmarkModel(db.Model):
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.String(36), primary_key=True)
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)