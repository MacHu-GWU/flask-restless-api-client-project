#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from marshmallow import Schema, fields

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

movie_and_genre = db.Table("movie_and_genre",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True),    
)

movie_and_director = db.Table("movie_and_director",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id")),
    db.Column("director_id", db.Integer, db.ForeignKey("person.id")),   
)
 
movie_and_writer = db.Table("movie_and_writer",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("writer_id", db.Integer, db.ForeignKey("person.id"), primary_key=True),   
)

movie_and_star = db.Table("movie_and_star",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("star_id", db.Integer, db.ForeignKey("person.id"), primary_key=True),   
)

person_and_role = db.Table("person_and_role",
    db.Column("person_id", db.Integer, db.ForeignKey("person.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),    
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode)
    maker_id = db.Column(db.Integer, db.ForeignKey("maker.id"))

    maker = db.relationship("Maker", 
        backref=db.backref("movies", lazy="dynamic"))
    genres = db.relationship("Genre", secondary="movie_and_genre",
        backref=db.backref("movies", lazy="dynamic"))
    directors = db.relationship("Person", secondary="movie_and_director",
        backref=db.backref("movies_as_director", lazy="dynamic"))
    writers = db.relationship("Person", secondary="movie_and_writer",
        backref=db.backref("movies_as_writer", lazy="dynamic"))
    stars = db.relationship("Person", secondary="movie_and_star",
        backref=db.backref("movies_as_star", lazy="dynamic"))
    
class Maker(db.Model):
    """
    
    Movie-to-Maker = many-to-one
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    
class Genre(db.Model):
    """
    Movie-to-Genre = many-to-many
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)


class Person(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    
    roles = db.relationship("Role", secondary="person_and_role",
        backref=db.backref("persons", lazy="dynamic"))
    
class Role(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

if __name__ == "__main__":    
    def run_api_server():
        # Create the database tables.
        db.create_all()
        
        # Create the Flask-Restless API manager.
        manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
        
        # Create API endpoints
        manager.create_api(Movie, collection_name="movie", 
                           methods=["GET", "POST", "PATCH", "DELETE"], 
                           allow_functions=True)
        manager.create_api(Maker, collection_name="maker", 
                           methods=["GET", "POST", "PATCH", "DELETE"], 
                           allow_functions=True)
        manager.create_api(Genre, collection_name="genre", 
                           methods=["GET", "POST", "PATCH", "DELETE"], 
                           allow_functions=True)
        manager.create_api(Person, collection_name="person", 
                           methods=["GET", "POST", "PATCH", "DELETE"], 
                           allow_functions=True)
        manager.create_api(Role, collection_name="role", 
                           methods=["GET", "POST", "PATCH", "DELETE"], 
                           allow_functions=True)
        # start the flask loop
        app.run()
        
    run_api_server()