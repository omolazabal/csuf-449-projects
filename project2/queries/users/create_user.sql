-- :name create_user :insert
INSERT INTO users(username, user_pass, disp_name, email, url_homepage)
VALUES(:username, :user_pass, :disp_name, :email, :url_homepage);
