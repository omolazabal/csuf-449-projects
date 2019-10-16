
# Tracks
echo 'New track'
curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/track.json \
     http://localhost:5000/tracks

echo 'Update track'
curl --verbose \
     --header "Content-type: application/json" \
     --request PATCH \
     --data @data/track_edit.json \
     http://localhost:5000/tracks/3

echo 'Get track'
curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5000/tracks/3

echo 'Delete track'
curl --verbose \
     --header "Content-type: application/json" \
     --request DELETE \
     http://localhost:5000/tracks/3

# Playlists
echo 'New playlist'
curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/playlist.json \
     http://localhost:5000/playlists

echo 'Get playlist'
curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5000/playlists/3

echo 'List all playlists'
echo 'Get playlist'
curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5000/playlists/all

echo 'List all playlists by user'
curl --verbose \
     --header "Content-type: application/json" \
     --request GET \
     http://localhost:5000/playlists?creator=username2

echo 'Delete playlist'
curl --verbose \
     --header "Content-type: application/json" \
     --request DELETE \
     http://localhost:5000/playlists/3

# # Users
# curl --verbose \
#      --header "Content-type: application/json" \
#      --request POST \
#      --data @data/sample_user.json \
#      http://localhost:5001/users
# 
# curl --verbose \
#      --header "Content-type: application/json" \
#      --request DELETE \
#      http://localhost:5001/users/3
# 
#      curl --verbose \
#      --header "Content-type: application/json" \
#      --request PUT \
#      --data @data/sample_user.json \
#      http://localhost:5001/users
# 
# curl --verbose \
#      --header "Content-type: application/json" \
#      --request GET \
#      http://localhost:5001/users/3
# 
# 
# # Descriptions
# curl --verbose \
#      --header "Content-type: application/json" \
#      --request POST \
#      --data @data/sample_description.json \
#      http://localhost:5003/descriptions
# 
# curl --verbose \
#      --header "Content-type: application/json" \
#      --request DELETE \
#      http://localhost:5003/descriptions/3
# 
#      curl --verbose \
#      --header "Content-type: application/json" \
#      --request PUT \
#      --data @data/sample_description.json \
#      http://localhost:5003/descriptions
# 
# curl --verbose \
#      --header "Content-type: application/json" \
#      --request GET \
#      http://localhost:5003/descriptions/3
