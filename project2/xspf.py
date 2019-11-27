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
	getPlaylist = "http://localhost:5001/playlists/" + str(id)
	playlists = requests.get(getPlaylist)

	# parses out the track section in the response
	print(playlists.status_code)
	if playlists.status_code == 200:
		urls = playlists.json()['track']
		print(playlists.json())
		print(urls)
		
		# renders xspf template file
		return render_template('playlist.xspf', urls=urls)
	else:
		return { "error" : f"Playlist with id {id} not found" }, status.HTTP_404_NOT_FOUND


if __name__ == "__main__":
	app.run(debug=True)