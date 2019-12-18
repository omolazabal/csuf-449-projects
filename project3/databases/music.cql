
DROP KEYSPACE IF EXISTS music
CREATE KEYSPACE music
  WITH REPLICATION = {
   'class' : 'SimpleStrategy',
   'replication_factor' : 1
  };


DROP COLUMNFAMILY IF EXISTS users;
CREATE COLUMNFAMILY users(
    uuid UUID PRIMARY KEY,
    username VARCHAR, 
    user_pass VARCHAR,
    disp_name VARCHAR,
    email VARCHAR,
    url_homepage TEXT,
    playlists_uuids LIST<UUID>,
    playlist_descriptions MAP<UUID, TEXT>,
    playlist_title MAP<UUID, TEXT>,
)

DROP COLUMNFAMILY tracks(
    uuid UUID PRIMARY KEY,
    title VARCHAR,
    album_title VARCHAR,
    artist VARCHAR,
    track_length FLOAT,
    media_file_url TEXT,
    album_art_url TEXT,
    playlists_uuids LIST<UUID>,
    track_description TEXT,
    descriptor_uuid UUID
)

