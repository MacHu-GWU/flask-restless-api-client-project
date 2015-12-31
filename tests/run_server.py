#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import flask.ext.sqlalchemy
import flask.ext.restless

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DB_FILE = ":memory:"
SQLALCHEMY_DATABASE_URI = "sqlite:///%s" % DB_FILE
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

db = flask.ext.sqlalchemy.SQLAlchemy(app)

# Create your Flask-SQLALchemy models
# User-to-Post is one-to-many
# Post-to-Tag is many-to-many
class User(db.Model):
    """一个User是一个用户, 一个用户可能发多个帖子。
    """
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode, nullable=False)
    birth_date = db.Column(db.Date)
    create_datetime = db.Column(db.DateTime)

# 关于many-to-many的正确实现部分, 请参考:
# http://flask-sqlalchemy.pocoo.org/2.1/models/#many-to-many-relationships
post_and_tag = db.Table("post_and_tag",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),    
)
    
class Post(db.Model):
    """一个Post是一个帖子, 一个帖子只能有一个作者。一个帖子能有多个标签。
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    body = db.Column(db.Unicode)
    create_datetime = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    author = db.relationship("User", backref=db.backref("articles", lazy="dynamic"))
    tags = db.relationship("Tag", secondary="post_and_tag", 
                           backref=db.backref("posts", lazy="dynamic"))
    
class Tag(db.Model):
    """一个Tag是一个标签。
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    
# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints
manager.create_api(User, collection_name="user", 
                   methods=["GET", "POST", "PATCH", "DELETE"], 
                   allow_functions=True)
manager.create_api(Post, collection_name="post", 
                   methods=["GET", "POST", "PATCH", "DELETE"], 
                   allow_functions=True)
manager.create_api(Tag, collection_name="tag", 
                   methods=["GET", "POST", "PATCH", "DELETE"], 
                   allow_functions=True)

# start the flask loop
app.run()