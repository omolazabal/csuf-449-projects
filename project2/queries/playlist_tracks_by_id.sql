-- :name playlist_tracks_by_id :many
SELECT media_file_url FROM playlist_tracks
WHERE playlist_id = :playlist_id;
