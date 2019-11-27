-- :name playlist_tracks_by_id :many
SELECT * FROM playlist_tracks
WHERE playlist_id = :playlist_id;
