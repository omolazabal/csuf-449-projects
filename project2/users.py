import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import werkzeug

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


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
	user = queries.user_by_username(username=username)
	if user:
		return user, status.HTTP_200_OK
	return { 'error' : f"User with username {username} not found" }, status.HTTP_404_NOT_FOUND


# DELETE a user
def delete_user(username):
	if not id:
		raise exceptions.ParseError()
	try:
		queries.delete_user(username=username)
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
		user['id'] = queries.create_user(**user)
	except Exception as e:
		return { 'error' : str(e) }, status.HTTP_409_CONFLICT
	return user, status.HTTP_201_CREATED

# PATCH user (update password)
def update_user(username, password):
	fields = ['user_pass']
	for field in password.keys():
		if field not in fields:
			return { 'error': f'key {field} does not exist' }, status.HTTP_404_NOT_FOUND
	updates = []
	query = 'UPDATE users SET'
	# print(password.items())
	for key, value in password.items():
		query += f' {key}=?,'
		updates.append(werkzeug.security.generate_password_hash(value, method='pbkdf2:sha256', salt_length=8))
	query = query[:-1] + ' WHERE username = ?;'
	# print(updates)
	updates.append(username)
	try:
		# print("query: ",query)
		# print("updates: ",updates)
		queries._engine.execute(query, updates)
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
		checkUser = queries.user_with_password(username=username)
		if not checkUser:
			return { 'error' : f"user with username '{username}' does not exist"}
		return { 'result' : werkzeug.check_password_hash(checkUser['user_pass'], user['user_pass']) }
	except Exception as e:
		return { 'error' : str(e) }, status.HTTP_409_CONFLICT


if __name__ == "__main__":
	app.run()







