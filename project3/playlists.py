
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
from flask_cassandra import CassandraCluster
import uuid

app = flask_api.FlaskAPI(__name__)
cassandra = CassandraCluster()
app.config.from_envvar('APP_CONFIG')
app.config['CASSANDRA_NODES'] = app.config['MUSIC_DATABASE_URL']

@app.route('/playlists/<uuid:id>', methods=['GET', 'DELETE'])
def playlist(id):
    if request.method == 'GET':
        return get_playlist(id)
    elif request.method == 'DELETE':
        return delete_playlist(id)

@app.route('/playlists', methods=['GET', 'POST'])
def playlists():
    if request.method == 'POST':
        return insert_playlist(request.data)
    elif request.method == 'GET':
        return get_playlists(request.args)

@app.route('/playlists/all', methods=['GET'])
def all_playlists():
    create_playlist_cql = (
            "SELECT * FROM PLAYLISTS"
    )
    session = cassandra.connect()
    session.set_keyspace("music")
    all_playlists = session.execute(create_playlist_cql)
    return list(all_playlists), status.HTTP_200_OK

def get_playlists(query_parameters):
    creator = query_parameters.get('creator')
    if not creator:
        return { 'error': 'argument "creator" missing' }, status.HTTP_400_BAD_REQUEST
    create_playlist_cql = (
            "SELECT * FROM PLAYLISTS "
            "WHERE creator=%s"
            " ALLOW FILTERING"
    )
    session = cassandra.connect()
    session.set_keyspace("music")
    all_playlists = session.execute(create_playlist_cql, (creator,))
    if all_playlists:
        return list(all_playlists), status.HTTP_200_OK
    return { "error" : f"Playlist with creator {creator} not found" }, status.HTTP_404_NOT_FOUND
        

def get_playlist(id):
    create_playlist_cql = (
            "SELECT * FROM PLAYLISTS "
            "WHERE uuid=%s"
            " ALLOW FILTERING"
    )
    session = cassandra.connect()
    session.set_keyspace("music")
    playlist = session.execute(create_playlist_cql, (id,))
    if playlist:
        return list(playlist), status.HTTP_200_OK
    return { "error" : f"Playlist with id {id} not found" }, status.HTTP_404_NOT_FOUND

def insert_playlist(playlist):
    response = jsonify()
    required_fields = ['title', 'creator', 'tracks', 'description']
    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        track_ids = playlist['tracks']
        del playlist['tracks']
        uid = uuid.uuid4()
        playlist['id'] = uid
        create_playlist_cql = (
                "INSERT INTO playlists(uuid, title, creator, description)"
                "VALUES(%s, %s, %s, %s)"
        )
        session = cassandra.connect()
        session.set_keyspace("music")
        session.execute(create_playlist_cql, (playlist['id'], playlist['title'], playlist['creator'], playlist['description']))

        num_tracks = 0
        for id in track_ids:
            num_tracks += 1
            cql = (
                    "UPDATE playlists "
                    "SET tracks = tracks + [%s] "
                    "WHERE uuid=%s"
            )
            session = cassandra.connect()
            session.set_keyspace("music")
            session.execute(cql, (uuid.UUID(id) ,playlist['id']))
        playlist['tracks'] = track_ids
        response = jsonify(playlist)
        response.headers['location'] = f'/playlists/{playlist["id"]}'
        response.status_code = 201
    except Exception as e:
        response = jsonify(error=str(e))
        response.status_code = 409
    return response

def delete_playlist(id):
    if not id:
        raise exceptions.ParseError()
    try:
        create_playlist_cql = (
                "DELETE FROM PLAYLISTS "
                "WHERE uuid=%s"
        )
        session = cassandra.connect()
        session.set_keyspace("music")
        session.execute(create_playlist_cql, (id,))
        return { 'message': f'Deleted 1 playlist with id {id}' }, status.HTTP_200_OK
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND

if __name__ == "__main__":
    app.run()

