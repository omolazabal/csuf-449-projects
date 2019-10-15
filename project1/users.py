import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


# Retrieves user information
@app.route('/users/<username>', methods=['GET', 'DELETE'])
def user(username):
	user = queries.user_by_username(username=username)
	if request.method == 'GET':
		if user:
			return user, status.HTTP_200_OK
		else:
			raise exceptions.NotFound()
	elif request.method == 'DELETE':
		return delete_user(username)


# Delete a user
def delete_user(username):
	if not id:
		raise exceptions.ParseError()
	try:
		queries.delete_user(username=username)
		return { 'message' : f'Deleted 1 user with username {username}' }, status.HTTP_200_OK
	except Exception as e:
		return { 'error' : str(e) }, status.HTTP_404_NOT_FOUND


# Create new user
@app.route('/users', methods=['POST'])
def users():
	if request.method == 'POST':
		return create_user(request.data)


def create_user(user):
	required_fields = ['username', 'user_pass', 'disp_name', 'email', 'url_homepage']
	if not all([field in user for field in required_fields]):
		raise exception.ParseError()
	try:
		user['id'] = queries.create_user(**user)
	except Exception as e:
		return { 'error' : str(e) }, status.HTTP_409_CONFLICT
	return user, status.HTTP_201_CREATED


if __name__ == "__main__":
	app.run()







