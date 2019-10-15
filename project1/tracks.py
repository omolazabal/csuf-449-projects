
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.route('/tracks/<int:id>', methods=['GET', 'DELETE'])
def track(id):
    track = queries.track_by_id(id=id)
    if request.method == 'GET':
        if track:
            return track
        else:
            raise exceptions.NotFound()
    elif request.method == 'DELETE':
        return delete_track(id)

@app.route('/tracks', methods=['POST', 'PATCH'])
def tracks():
    if request.method == 'POST':
        return insert_track(request.data)
    # elif request.method == 'PATCH':
    #     return update_track(request.args)

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

# def update_track(query_parameters):
#     _id = query_parameters.get('id')
#     title = query_parameters.get('title')
#     album_title = query_parameters.get('album_title')
#     time_len = query_parameters.get('time_len')
#     url_media_file = query_parameters.get('url_media_file')
#     url_album_chart = query_parameters.get('url_album_chart')

if __name__ == "__main__":
    app.run()

