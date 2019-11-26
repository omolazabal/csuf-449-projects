-- :name delete_track :affected
DELETE FROM tracks
WHERE uuid = :id;
