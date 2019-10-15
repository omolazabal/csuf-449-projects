
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.route('/tracks/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def track(id):
    if request.method == 'GET':
        return get_track(id)
    elif request.method == 'DELETE':
        return delete_track(id)
    elif request.method == 'PATCH':
        return update_track(id, request.data)

@app.route('/tracks', methods=['POST'])
def tracks():
    return insert_track(request.data)

def get_track(id):
    track = queries.track_by_id(id=id)
    if track:
        return track
    else:
        raise exceptions.NotFound()

def insert_track(track):
    required_fields = ['title', 'album_title', 'time_len', 'url_media_file', 'url_album_chart']
    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        track['id'] = queries.create_track(**track)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    return track, status.HTTP_201_CREATED

def delete_track(id):
    if not id:
        raise exceptions.ParseError()
    try:
        queries.delete_track(id=id)
        return { 'message': f'Deleted 1 track with id {id}' }, status.HTTP_200_OK
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

def update_track(id, track):
    fields = ['title', 'album_title', 'time_len', 'url_media_file', 'url_album_chart']
    for field in track.keys():
        if field not in fields:
            raise exceptions.ParseError()
    updates = []
    query = 'UPDATE tracks SET'
    for key, value in track.items():
        query += f' {key}=?,'
        updates.append(value)
    query = query[:-1] + ' WHERE id = ?;'
    updates.append(id)
    queries._engine.execute(query, updates)
    track = get_track(id)
    return track, status.HTTP_200_OK

if __name__ == "__main__":
    app.run()

