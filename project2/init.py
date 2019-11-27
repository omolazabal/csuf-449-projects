
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import os

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = [
    pugsql.module('queries/users'),
    pugsql.module('queries/tracks1/'),
    pugsql.module('queries/tracks2/'),
    pugsql.module('queries/tracks3/')
]

queries[0].connect(app.config['MUSIC_DATABASE_URL'])
queries[1].connect(app.config['TRACKS1_DATABASE_URL'])
queries[2].connect(app.config['TRACKS2_DATABASE_URL'])
queries[3].connect(app.config['TRACKS3_DATABASE_URL'])

@app.cli.command('init')
def init_db():
    os.system('rm -f music.db')
    os.system('rm -f tracksdb1.db')
    os.system('rm -f tracksdb2.db')
    os.system('rm -f tracksdb3.db')
    with app.app_context():
        tracks1_db = queries[1]._engine.raw_connection()
        with app.open_resource('databases/tracksdb1.sql', mode='r') as f:
            tracks1_db.cursor().executescript(f.read())
        tracks1_db.commit()

        tracks2_db = queries[2]._engine.raw_connection()
        with app.open_resource('databases/tracksdb2.sql', mode='r') as f:
            tracks2_db.cursor().executescript(f.read())
        tracks2_db.commit()

        tracks3_db = queries[3]._engine.raw_connection()
        with app.open_resource('databases/tracksdb3.sql', mode='r') as f:
            tracks3_db.cursor().executescript(f.read())
        tracks3_db.commit()

        tracks4_db = queries[0]._engine.raw_connection()
        with app.open_resource('databases/music.sql', mode='r') as f:
            tracks4_db.cursor().executescript(f.read())
        tracks4_db.commit()
    

if __name__ == "__main__":
    app.run()
