
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('music.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/tracks/<int:id>', methods=['GET'])
def get_track(id):
    track = queries.track_by_id(id=id)
    if track:
        return track
    else:
        raise exceptions.NotFound()


app.run()
