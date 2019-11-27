-- :name insert_playlist_tracks :affected
INSERT INTO playlist_tracks(playlist_id, track_id)
VALUES(:playlist_id, :track_id)
