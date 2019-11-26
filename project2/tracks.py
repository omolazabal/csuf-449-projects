
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import uuid
import pugsql
import sqlite3 

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

#queries = pugsql.module('queries/')

#needd to create 3 mode modules here 
queries2 = pugsql.module('queries2/')
queries3 = pugsql.module('queries3/')
queries4 = pugsql.module('queries4/')
#queries.connect(app.config['DATABASE_URL'])
queries2.connect(app.config['DATABASE_URL2'])
queries3.connect(app.config['DATABASE_URL3'])
queries4.connect(app.config['DATABASE_URL4'])



sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)


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
    import pprint
    pprint.pprint(id)
    if   id.int % 3 ==0:
        track = queries2.track_by_id(id=id)
    elif id.int % 3 ==1:
        track = queries3.track_by_id(id=id)
    elif id.int  % 3 == 2:
        track = queries4.track_by_id(id=id)
    
    if track:
        return track, status.HTTP_200_OK
    return { "error" : f"Track with id {id} not found" }, status.HTTP_404_NOT_FOUND

def insert_track(track):
    # POST
    response = jsonify()
    required_fields = ['track_title', 'album_title', 'artist', 'track_length', 'media_file_url', 'album_art_url']
    if not all([field in track for field in required_fields]):
        response = jsonify(error="invalid fields")
        response.status_code = 409
    else:
        try:
            id = uuid.uuid4()
            track['id'] = id
            print(track['id'])
            import pprint
            pprint.pprint(track)
            if id.int % 3 == 0:
                queries2.create_track(**track)
            elif id.int%3 == 1:
                queries3.create_track(**track)
            elif id.int %3 == 2:
                queries4.create_track(**track)
            response = jsonify(track)
            response.headers['location'] = f'/tracks/{track["id"]}'
            response.status_code = 201
        except Exception as e:
            response = jsonify(error=str(e))
            response.status_code = 409
    return response

def delete_track(id):
    # DELETE
    if not id:
        raise exceptions.ParseError()
    try:
        if id % 3 == 0:
            queries2.delete_track(id=id)
        elif id%3 == 1:
            queries3.delete_track(id=id)
        elif id%3 == 2:
            queries4.delete_track(id=id)
        return { 'message': f'Deleted 1 track with id {id}' }, status.HTTP_200_OK
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND

def update_track(id, track):
    # PATCH
    if len(track) == 0:
            return { 'error': f'key not specified' }, status.HTTP_404_NOT_FOUND
    fields = ['track_title', 'album_title', 'artist', 'track_length', 'media_file_url', 'album_art_url']
    for field in track.keys():
        if field not in fields:
            return { 'invalid key': f'{field}' }, status.HTTP_404_NOT_FOUND
    updates = []
    query = 'UPDATE tracks SET'
    for key, value in track.items():
        query += f' {key}=?,'
        updates.append(value)
    query = query[:-1] + ' WHERE uuid = ?;'
    track['id'] = id
    updates.append(id)
    try:
        if int(id)%3 ==0:
            queries2._engine.execute(query, updates)
        elif int(id)%3 == 1:
            queries3._engine.execute(query, updates)
        elif int(id)%3 ==2:
            queries4._engine.execute(query, updates)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
    return get_track(id)

if __name__ == "__main__":
    app.run()

