# curl --header "Content-type: application/json" --request PUT --data '{"id": 1, "title": "this is a title", "album": "this ia an album", "time_len": 4.57, "url_media_file": "This is a media file", "url_album_chart": "7"}' 
# curl --header "Content-type: application/json" --request PUT --data '{"id": 2, "title": "this is a title2", "album": "this ia an album2", "time_len": 4.58, "url_media_file": "This is a media file2", "url_album_chart": "78"}' 
# curl --header "Content-type: application/json" --request DELETE --data '{"id": 2, "title": "this is a title2", "album": "this ia an album2", "time_len": 4.58, "url_media_file": "This is a media file2", "url_album_chart": "78"}' 
# curl --header "Content-type: application/json" --request GET --data '{"id": 2, "title": "}'

curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/sample_track.json \
     http://localhost:5000/tracks

curl --verbose \
     --header "Content-type: application/json" \
     --request DELETE \
     http://localhost:5000/tracks?id=3
