-- :name create_track :insert
INSERT INTO tracks(track_title, album_title, artist, track_length, media_file_url, album_art_url)
VALUES(:track_title, :album_title, :artist, :track_length, :media_file_url, :album_art_url)
