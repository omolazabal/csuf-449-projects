# curl --header "Content-type: application/json" --request PUT --data '{"id": 1, "title": "this is a title", "album": "this ia an album", "time_len": 4.57, "url_media_file": "This is a media file", "url_album_chart": "7"}' 
# curl --header "Content-type: application/json" --request PUT --data '{"id": 2, "title": "this is a title2", "album": "this ia an album2", "time_len": 4.58, "url_media_file": "This is a media file2", "url_album_chart": "78"}' 
# curl --header "Content-type: application/json" --request DELETE --data '{"id": 2, "title": "this is a title2", "album": "this ia an album2", "time_len": 4.58, "url_media_file": "This is a media file2", "url_album_chart": "78"}' 
# curl --header "Content-type: application/json" --request GET --data '{"id": 2, "title": "}'
curl --verbose \
     --header "Content-type: application/json" \
     --request POST \
     --data @data/sample_track.json \
     http://localhost:5000/Tracks

curl --verbose \
     --header "content-type:application/json" \
     --requeest GET\
     --data @data/sample_track.json\
     http://localhost:5001/User



curl --verbose \
     --header "content-type:application/json" \
     --requeest DELETE\
     --data @data/sample_track.json\
     http://localhost:5002/Playlist



curl --verbose \
     --header "content-type:application/json" \
     --requeest PUT\
     --data @data/sample_track.json\
     http://localhost:5003/Descriptons




# we need to make seperate jaon files for every sample look in the data directory nd we will find what to do basically its a quick 5 minute thing
