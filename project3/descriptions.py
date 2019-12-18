import flask_api
import uuid
from flask import request
from flask_api import status, exceptions
from flask_cassandra import CassandraCluster

app = flask_api.FlaskAPI(__name__)
cassandra = CassandraCluster()
app.config.from_envvar('APP_CONFIG')
app.config['CASSANDRA_NODES'] = app.config['MUSIC_DATABASE_URL']


@app.route('/descriptions/<uuid:id>', methods=['GET'])
def description(id):
        cql = (
                "SELECT track_description, descriptor, uuid FROM tracks "
                "WHERE uuid=%s"
                " ALLOW FILTERING"
        )
        session = cassandra.connect()
        session.set_keyspace("music")
        description = list(session.execute(cql, (id,)))
        if description:
                return description
        else:
                raise exceptions.NotFound()

@app.route('/descriptions', methods=['POST'])
def descriptions():
        print('test')
        if request.method == 'POST':
                return insert_description(request.data)

def insert_description(description):
        required_fields = ['id', 'user_name', 'description']
        if not all([field in description for field in required_fields]):
                raise exceptions.ParseError()
        try:
                cql = (
                        "UPDATE tracks "
                        "SET descriptor=%s, track_description=%s "
                        "WHERE uuid=%s"
                )
                session = cassandra.connect()
                session.set_keyspace("music")
                session.execute(cql, (description['user_name'], description['description'], uuid.UUID(description['id'])))
        except Exception as e:
                return { 'error' : str(e) }, status.HTTP_409_CONFLICT

        return description, status.HTTP_201_CREATED

if __name__ == "__main__":
        app.run()




