-- :name user_with_password :one
SELECT username,user_pass FROM users
WHERE username = :username;
