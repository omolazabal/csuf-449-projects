-- :name playlist_by_creator :many
SELECT * FROM playlists
WHERE creator = :creator;
