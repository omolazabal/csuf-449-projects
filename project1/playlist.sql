-- $ sqlite3 playlist.db < sqlite.sql

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id INTEGER primary key,
    title VARCHAR NOT NULL,
    album_title VARCHAR NOT NULL,
    time_len FLOAT NOT NULL,
    url_media_file TEXT NOT NULL,
    url_album_chart TEXT NULL

);
DROP TABLE IF EXISTS playlist;

CREATE TABLE playlist(
    id INTEGER primary key,
    title VARCHAR NOT NULL,
    url_ind_tracks BLOB NOT NULL,
    username VARCHAR NOT NULL ,
    descript TEXT NULL,
    UNIQUE(username)

);

DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id INTEGER primary key,
    username VARCHAR NOT NULL , 
    user_pass VARCHAR NOT NULL,
    disp_name VARCHAR NOT NULL ,
    url_homepage TEXT NULL,
    UNIQUE(username, disp_name)
);

DROP TABLE IF EXISTS microservice;

CREATE TABLE microservice (
    id INTEGER primary key,
    user_description TEXT NULL,
    retrive_descipttion TEXT NULL
    


);
