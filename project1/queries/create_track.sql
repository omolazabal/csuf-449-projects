-- :name create_track :insert
INSERT INTO tracks(track_title, album_title, artist, time_length, media_file_url, album_art_url)
VALUES(:track_title, :album_title, :artist, :time_length, :url_media_file, :album_art_url)
