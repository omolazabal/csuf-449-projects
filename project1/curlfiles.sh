
# Tracks
curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/sample_track.json \
     http://localhost:5000/tracks

curl --verbose \
     --header "Content-type: application/json" \
     --request DELETE \
     http://localhost:5000/tracks/1

     curl --verbose \
     --header "Content-type: application/json" \
     --request PUT \
     --data @data/sample_track.json \
     http://localhost:5000/tracks/3

curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5000/tracks/3


# Users
curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/sample_user.json \
     http://localhost:5001/users

curl --verbose \
     --header "Content-type: application/json" \
     --request DELETE \
     http://localhost:5001/users/3

     curl --verbose \
     --header "Content-type: application/json" \
     --request PUT \
     --data @data/sample_user.json \
     http://localhost:5001/users

curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5001/users/3


# Playlists
curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/sample_playlist.json \
     http://localhost:5002/playlists

curl --verbose \
     --header "Content-type: application/json" \
     --request DELETE \
     http://localhost:5002/playlists/3

     curl --verbose \
     --header "Content-type: application/json" \
     --request PUT \
     --data @data/sample_playlist.json \
     http://localhost:5002/playlists

curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5002/playlists/3


# Descriptions
curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/sample_description.json \
     http://localhost:5003/descriptions

curl --verbose \
     --header "Content-type: application/json" \
     --request DELETE \
     http://localhost:5003/descriptions/3

     curl --verbose \
     --header "Content-type: application/json" \
     --request PUT \
     --data @data/sample_description.json \
     http://localhost:5003/descriptions

curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5003/descriptions/3
