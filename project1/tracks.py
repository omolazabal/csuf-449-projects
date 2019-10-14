
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.route('/tracks/<int:id>', methods=['GET'])
def track(id):
    track = queries.track_by_id(id=id)
    if track:
        return track
    else:
        raise exceptions.NotFound()

@app.route('/tracks', methods=['PUT', 'POST'])
def tracks():
    if request.method == 'POST':
        return insert_track(request.data)
    elif request.method == 'PUT':
        return None

def insert_track(track):
    required_fields = ['title', 'album_title', 'time_len', 'url_media_file', 'url_album_chart']
    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        track['id'] = queries.create_track(**track)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return track, status.HTTP_201_CREATED

if __name__ == "__main__":
    app.run()
