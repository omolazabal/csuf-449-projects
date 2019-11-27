-- :name delete_playlist :affected
DELETE FROM playlists 
WHERE id = :id;
