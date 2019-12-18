
import flask_api
from flask import request
from flask_api import status, exceptions
from flask_cassandra import CassandraCluster
import os

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
app.config['CASSANDRA_NODES'] = app.config['MUSIC_DATABASE_URL']

@app.cli.command('init')
def init_db():
    create_keyspace_cql = (
        "DROP KEYSPACE IF EXISTS music"
        "CREATE KEYSPACE music"
        "WITH REPLICATION = {"
        "'class' : 'SimpleStrategy',"
        "'replication_factor' : 1"
        "};"
    )
    create_users_cql = (
        "DROP COLUMNFAMILY IF EXISTS users;"
        "CREATE COLUMNFAMILY users("
        "    uuid UUID PRIMARY KEY,"
        "    username VARCHAR, "
        "    user_pass VARCHAR,"
        "    disp_name VARCHAR,"
        "    email VARCHAR,"
        "    url_homepage TEXT,"
        "    playlists_uuids LIST<UUID>,"
        "    playlist_descriptions MAP<UUID, TEXT>,"
        "    playlist_title MAP<UUID, TEXT>,"
        ");"
    )

    create_tracks_cql = (
        "DROP COLUMNFAMILY tracks("
        "    uuid UUID PRIMARY KEY,"
        "    title VARCHAR,"
        "    album_title VARCHAR,"
        "    artist VARCHAR,"
        "    track_length FLOAT,"
        "    media_file_url TEXT,"
        "    album_art_url TEXT,"
        "    playlists_uuids LIST<UUID>,"
        "    track_description TEXT,"
        "    descriptor_uuid UUID"
        ")"
    )

    session = cassandra.connect()
    session.execute(create_keyspace_cql)
    session.set_keyspace("music")
    session.execute(create_users_cql)
    session.execute(create_tracks_cql)

if __name__ == "__main__":
    app.run()
