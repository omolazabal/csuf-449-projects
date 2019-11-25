-- :name delete_user :affected
DELETE FROM users 
WHERE username = :username;
