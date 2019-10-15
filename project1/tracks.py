
import flask_api
from flask import request, jsonify
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
    # GET
    track = queries.track_by_id(id=id)
    if track:
        return track, status.HTTP_200_OK
    return { "error" : f"Track with id {id} not found" }, status.HTTP_404_NOT_FOUND

def insert_track(track):
    # POST
    response = jsonify()
    required_fields = ['track_title', 'album_title', 'time_length', 'media_file_url', 'album_art_url']
    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        track['id'] = queries.create_track(**track)
        response.headers['location'] = f'/tracks/{track["id"]}'
        response.status_code = 201
    except Exception as e:
        response.status_code = 409
    return response

def delete_track(id):
    # DELETE
    if not id:
        raise exceptions.ParseError()
    try:
        queries.delete_track(id=id)
        return { 'message': f'Deleted 1 track with id {id}' }, status.HTTP_200_OK
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND

def update_track(id, track):
    # PATCH
    fields = ['track_title', 'album_title', 'time_length', 'media_file_url', 'album_chart_url']
    for field in track.keys():
        if field not in fields:
            return { 'error': f'key {field} does not exist' }, status.HTTP_404_NOT_FOUND
    updates = []
    query = 'UPDATE tracks SET'
    for key, value in track.items():
        query += f' {key}=?,'
        updates.append(value)
    query = query[:-1] + ' WHERE id = ?;'
    updates.append(id)
    try:
        queries._engine.execute(query, updates)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
    return get_track(id)

if __name__ == "__main__":
    app.run()

