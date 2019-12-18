import flask_api
from flask import request
from flask_api import status, exceptions
from flask_cassandra import CassandraCluster
import werkzeug
import uuid

app = flask_api.FlaskAPI(__name__)
cassandra = CassandraCluster()
app.config.from_envvar('APP_CONFIG')
app.config['CASSANDRA_NODES'] = app.config['MUSIC_DATABASE_URL']


# endpoint for get user info, update password, delete user
@app.route('/users/<username>', methods=['GET', 'PATCH', 'DELETE'])
def user(username):
        if request.method == 'GET':
                return get_user(username)
        elif request.method == 'PATCH':
                return update_user(username, request.data)
        elif request.method == 'DELETE':
                return delete_user(username)


# GET a user
def get_user(username):
        get_user_cql = (
                "SELECT username, disp_name, email, url_homepage FROM users "
                ' WHERE username=%s ALLOW FILTERING'
        )
        session = cassandra.connect()
        session.set_keyspace("music")
        user = list(session.execute(get_user_cql, (username,))[0])
        if user:
                return user, status.HTTP_200_OK
        return { 'error' : f"User with username {username} not found" }, status.HTTP_404_NOT_FOUND


# DELETE a user
def delete_user(username):
        if not id:
                raise exceptions.ParseError()
        try:
                delete_user_cql = (
                        "DELETE FROM users "
                        'WHERE username = %s'
                )
                session = cassandra.connect()
                session.set_keyspace("music")
                session.execute(delete_user_cql, (username,))
                return { 'message' : f'Deleted 1 user with username {username}' }, status.HTTP_200_OK
        except Exception as e:
                return { 'error' : str(e) }, status.HTTP_404_NOT_FOUND


# endpoint for creating new user
@app.route('/users', methods=['POST'])
def users():
        if request.method == 'POST':
                return create_user(request.data)


# CREATE new user
def create_user(user):
        required_fields = ['username', 'user_pass', 'disp_name', 'email', 'url_homepage']
        if not all([field in user for field in required_fields]):
                raise exceptions.ParseError()
        try:
                user['user_pass'] = werkzeug.security.generate_password_hash(user['user_pass'], method='pbkdf2:sha256', salt_length=8)
                id = uuid.uuid4()
                user['uuid'] = id
                create_user_cql = (
                        "INSERT INTO users(uuid, username, user_pass, disp_name, email, url_homepage)"
                        "VALUES(%s, %s, %s, %s, %s, %s)"
                )
                session = cassandra.connect()
                session.set_keyspace("music")
                session.execute(create_user_cql, (user['uuid'], user['username'], user['user_pass'], user['disp_name'], user['email'], user['url_homepage']))
        except Exception as e:
                return { 'error' : str(e) }, status.HTTP_409_CONFLICT
        return user, status.HTTP_201_CREATED

# PATCH user (update password)
def update_user(username, password):
        fields = ['user_pass']
        for field in password.keys():
                if field not in fields:
                        return { 'error': f'key {field} does not exist' }, status.HTTP_404_NOT_FOUND
        query = (
            "UPDATE users SET user_pass=%s "
            ' WHERE username=%s'
        )
        pw = werkzeug.security.generate_password_hash(password['user_pass'], method='pbkdf2:sha256', salt_length=8)
        try:
                session = cassandra.connect()
                session.set_keyspace("music")
                session.execute(query, (pw, username))
        except Exception as e:
                return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
        return get_user(username)


# endpoint for authenticating user
@app.route('/users/authenticate', methods=['GET'])
def auth_user():
        return authenticate_user(request.data)


# AUTHENTICATE user
def authenticate_user(user):
        fields = ['username', 'user_pass']
        for field in user.keys():
                if field not in fields:
                        return { 'error' : f'key {field} does not exist' }, status.HTTP_404_NOT_FOUND
        try:
                username = user['username']
                auth_user_cql = (
                        "SELECT username, user_pass"
                        " FROM users"
                        " WHERE username=%s"
                )
                session = cassandra.connect()
                session.set_keyspace("music")
                checkUser = session.execute(auth_user_cql, (username,))[0]
                print(type(checkUser))
                if not checkUser:
                        return { 'error' : f"user with username '{username}' does not exist"}
                return { 'result' : werkzeug.check_password_hash(checkUser.user_pass, user['user_pass']) }
        except Exception as e:
                return { 'error' : str(e) }, status.HTTP_409_CONFLICT


if __name__ == "__main__":
        app.run()







