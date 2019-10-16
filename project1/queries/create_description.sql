-- :name create_description :insert
INSERT INTO descriptions(track_id, user_username, description)
VALUES(:track_id, :user_username, :description);
