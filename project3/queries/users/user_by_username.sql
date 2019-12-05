-- :name user_by_username :one
SELECT username,disp_name,email,url_homepage FROM users
WHERE username = :username;
