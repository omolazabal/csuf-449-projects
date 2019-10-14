-- :name create_track :insert
INSERT INTO tracks(title, album_title, time_len, url_media_file, url_album_chart)
VALUES(:title, :album_title, :time_len, :url_media_file, :url_album_chart)
