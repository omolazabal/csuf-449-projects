
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import os

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries2 = pugsql.module('queries2/')
queries3 = pugsql.module('queries3/')
queries4 = pugsql.module('queries4/')
queries.connect(app.config['DATABASE_URL'])
queries2.connect(app.config['DATABASE_URL2'])
queries3.connect(app.config['DATABASE_URL3'])
queries4.connect(app.config['DATABASE_URL4'])

@app.cli.command('init')
def init_db():
    os.system('rm -f music.db')
    os.system('rm -f tracksdb1.db')
    os.system('rm -f tracksdb2.db')
    os.system('rm -f tracksdb3.db')
    with app.app_context():
        db1 = queries2._engine.raw_connection()
        with app.open_resource('databases/tracksdb1.sql', mode='r') as f:
            db1.cursor().executescript(f.read())
        db1.commit()
        db2 = queries3._engine.raw_connection()
        with app.open_resource('databases/tracksdb2.sql', mode='r') as f:
            db2.cursor().executescript(f.read())
        db2.commit()
        db3 = queries4._engine.raw_connection()
        with app.open_resource('databases/tracksdb3.sql', mode='r') as f:
            db3.cursor().executescript(f.read())
        db3.commit()
        db4 = queries._engine.raw_connection()
        with app.open_resource('databases/music.sql', mode='r') as f:
            db4.cursor().executescript(f.read())
        db4.commit()
    

if __name__ == "__main__":
    app.run()
