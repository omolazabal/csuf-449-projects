
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

@app.route('/playlists/<int:id>', methods=['GET', 'DELETE'])
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
    all_playlists = list(queries.all_playlists())
    for index, playlist in enumerate(all_playlists):
        tracks = list(queries.playlist_tracks_by_id(playlist_id=playlist['id']))
        tracks = [track['media_file_url'] for track in tracks]
        all_playlists[index]['tracks'] = tracks
    return all_playlists, status.HTTP_200_OK

def get_playlists(query_parameters):
    creator = query_parameters.get('creator')
    if not creator:
        return { 'error': 'argument "creator" missing' }, status.HTTP_400_BAD_REQUEST
    playlists = list(queries.playlist_by_creator(creator=creator))
    if playlists:
        for index, playlist in enumerate(playlists):
            tracks = list(queries.playlist_tracks_by_id(playlist_id=playlist['id']))
            tracks = [track['media_file_url'] for track in tracks]
            playlists[index]['tracks'] = tracks
        return playlists, status.HTTP_200_OK
    return { "error" : f"Playlist with creator {creator} not found" }, status.HTTP_404_NOT_FOUND
        

def get_playlist(id):
    playlist = queries.playlist_by_id(id=id)
    if playlist:
        tracks = list(queries.playlist_tracks_by_id(playlist_id=id))
        tracks = [track['media_file_url'] for track in tracks]
        playlist['track'] = tracks
        return playlist, status.HTTP_200_OK
    return { "error" : f"Playlist with id {id} not found" }, status.HTTP_404_NOT_FOUND

def insert_playlist(playlist):
    response = jsonify()
    required_fields = ['title', 'creator', 'tracks', 'description']
    if not all([field in playlist for field in required_fields]):
        raise exceptions.ParseError()
    try:
        track_urls = playlist['tracks']
        del playlist['tracks']
        playlist['id'] = queries.create_playlist(**playlist)
        num_tracks = 0
        for url in track_urls:
            with queries.transaction():
                queries.enable_foreign_keys()
                num_tracks += queries.insert_playlist_tracks(playlist_id=playlist['id'], media_file_url=url)
        playlist['tracks'] = track_urls
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
        with queries.transaction():
            queries.enable_foreign_keys()
            queries.delete_playlist(id=id)
        return { 'message': f'Deleted 1 playlist with id {id}' }, status.HTTP_200_OK
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND

if __name__ == "__main__":
    app.run()

