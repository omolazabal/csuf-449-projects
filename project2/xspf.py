import flask_api
import requests
from playlists import get_playlist
from flask import render_template
from flask_api import status

app = flask_api.FlaskAPI(__name__, template_folder='')
app.config.from_envvar('APP_CONFIG')

# currently only gets the playlist with specific id
@app.route('/playlist/<int:id>')
def playlist(id):
	# concatenate the string so that we can put a get request for the right id
	getPlaylist = "http://localhost:5100/playlists/" + str(id)
	# remove .json() and uncomment bottom block for alternate way if this doesn't work
	playlists = requests.get(getPlaylist).json()

	# parses out the track section in the response
	print(playlists.status_code)
	if playlists.status_code == 200:
		track_ids = playlists.json()['track']
		get_track = []
		for track_id in track_ids:
			# get each individual track object from calling a get request on tracks + the track id
			# requires get request on tracks endpoint to work while passing in the track_id
			track = requests.get("http://localhost:5000/tracks/" + str(track_id)).json()
			
			# get track description and make it another entry in the dictionary so we can parse it out later
			track['description'] = request.get("http://localhost:5003/descriptions" + str(track_id)).json()
			get_track.append(track)

		# alternat if `requests.get(getPlaylist).json()` does not work
		# creator = playlists.json()['creator']
		# title = playlists.json()['title']
		# description = playlists.json()['description']
		print(playlists)
		print(get_tracks)

		# renders xspf template file
		return render_template('playlist.xspf', playlist=playlists, tracks=get_track)
	else:
		return { "error" : f"Playlist with id {id} not found" }, status.HTTP_404_NOT_FOUND

if __name__ == "__main__":
	app.run(debug=True)