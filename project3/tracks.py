
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import uuid
from flask_cassandra import CassandraCluster

app = flask_api.FlaskAPI(__name__)
cassandra = CassandraCluster()
app.config.from_envvar('APP_CONFIG')
app.config['CASSANDRA_NODES'] = app.config['MUSIC_DATABASE_URL']

@app.route('/tracks/<uuid:id>', methods=['GET', 'DELETE', 'PATCH'])
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
    cql = (
            "SELECT * FROM tracks "
            "WHERE uuid=%s"
            " ALLOW FILTERING"
    )
    session = cassandra.connect()
    session.set_keyspace("music")
    track = session.execute(cql, (id,))
    if track:
        return list(track), status.HTTP_200_OK
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
            cql = (
                    "INSERT INTO tracks(uuid, title, album_title, artist, track_length, media_file_url, album_art_url)"
                    "VALUES(%s, %s, %s, %s, %s,%s,%s)"
            )
            session = cassandra.connect()
            session.set_keyspace("music")
            session.execute(cql, (id, track['track_title'], track['album_title'], track['artist'], track['track_length'], track['media_file_url'], track['album_art_url']))
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
        cql = (
                "DELETE FROM tracks "
                "WHERE uuid=%s"
        )
        session = cassandra.connect()
        session.set_keyspace("music")
        session.execute(cql, (id,))
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
        query += f' {key}=%s,'
        updates.append(value)
    query = query[:-1] + ' WHERE uuid = %s;'
    track['id'] = id
    updates.append(id)
    try:
        session = cassandra.connect()
        session.set_keyspace("music")
        session.execute(query, updates)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
    return get_track(id)

if __name__ == "__main__":
    app.run()

