from api.app import db
import genre, country

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    quality = db.Column(db.String(300))
    duration = db.Column(db.String(300))
    description = db.Column(db.String(400))
    stars = db.Column(db.String(300))
    url = db.Column(db.String(300))
    release = db.Column(db.Integer)
    ratings = db.Column(db.Float)
    img = db.Column(db.String(300))


    genre = db.relationship("Genre", lazy="dynamic")
    country = db.relationship("Country", lazy="dynamic")

    def __init__(self, title, quality, duration, description,
                 stars, url, release, img, ratings):
        self.title = title
        self.quality = quality
        self.duration = duration
        self.description = description
        self.stars = stars
        self.ratings = ratings
        self.url = url
        self.release = release
        self.img = img

    def __str__(self):
        return "<Film(%(title)s, %(url)s)>" % self.__dict__
