
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('music.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    pass

def create_track():
    pass

def delete_track():
    pass

def edit_track():
    pass

app.run()
