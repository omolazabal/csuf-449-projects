-- :name track_by_id :one
SELECT * FROM tracks
WHERE uuid = :id;
