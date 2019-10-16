-- :name insert_playlist_tracks :affected
INSERT INTO playlist_tracks(playlist_id, media_file_url)
VALUES(:playlist_id, :media_file_url)
