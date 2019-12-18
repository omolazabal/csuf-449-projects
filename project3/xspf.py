import flask_api
import requests
from playlists import get_playlist
from flask import render_template, make_response
from flask_api import status
from pymemcache.client import base

app = flask_api.FlaskAPI(__name__, template_folder='')
app.config.from_envvar('APP_CONFIG')

# currently only gets the playlist with specific id
@app.route('/playlist/<uuid:id>.xspf')
def playlist(id):
        #run memcached
        client = base.Client(('localhost',11211))
        result = client.get(str(id))
        if result is None:
                getPlaylist = "http://localhost:8000/playlists/" + str(id)
                result = requests.get(getPlaylist)
                client.set(str(id),result,60)
                playlists = requests.get(getPlaylist).json()
        else:
                getPlaylist = "http://localhost:8000/playlists/" + str(id)
                playlists = requests.get(getPlaylist).json()

        track_ids = playlists[0]['tracks']
        get_track = []
        for track_id in track_ids:
                track = requests.get("http://localhost:8000/tracks/" + str(track_id)).json()[0]
                track['description'] = requests.get("http://localhost:8000/descriptions/" + str(track_id)).json()[0]
                get_track.append(track)

        # renders xspf template file
        template = render_template('playlist.xspf', playlist=playlists, tracks=get_track)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xspf'
        return response

if __name__ == "__main__":
        app.run(debug=True)
