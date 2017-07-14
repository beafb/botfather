from api.app import db
import film, country

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    film_id = db.Column(db.Integer, db.ForeignKey("film.id"))

    #film = db.relationship("Genre", lazy="dynamic")


    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<Genre(%(film_id)s, %(name)s)>" % self.__dict__