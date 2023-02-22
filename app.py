# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace("movies")


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):
        if request.args.get("genre_id"):
            movies = Movie.query.filter_by(genre_id=request.args.get("genre_id")).all()
            movies_schema = MovieSchema(many=True)
            return movies_schema.dump(movies), 200

        elif request.args.get("director_id"):
            movies = Movie.query.filter_by(director_id=request.args.get("director_id")).all()
            movies_schema = MovieSchema(many=True)
            return movies_schema.dump(movies), 200
        else:
            movies = Movie.query.all()
            movies_schema = MovieSchema(many=True)
            return movies_schema.dump(movies), 200


@movie_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        movie_schema = MovieSchema()
        return movie_schema.dump(movie), 200


if __name__ == '__main__':
    app.run(debug=True)
