from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_restless
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://localhost/botfather")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

methods = ['GET', 'POST', 'PATCH', 'DELETE']

from models.film import Film
from models.genre import Genre
from models.country import Country

manager.create_api(Film, methods=methods,
                   allow_patch_many=True,
                   allow_delete_many=True,
                   primary_key='id',
                   max_results_per_page=10000
                   )
manager.create_api(Genre, methods=methods,
                   allow_patch_many=True,
                   allow_delete_many=True
                   )
manager.create_api(Country, methods=methods,
                   allow_patch_many=True,
                   allow_delete_many=True
                   )


@app.route('/drop_all')
def drop_all():
    db.drop_all()
    return "OK"


@app.route('/create_all')
def create_all():
    db.create_all()
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)

