import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/descriptions')
queries.connect(app.config['MUSIC_DATABASE_URL'])


@app.route('/descriptions/<uuid:id>', methods=['GET'])
def description(id):
	description = queries.description_by_track_id(track_id=id)
	if description:
		return description
	else:
		raise exceptions.NotFound()

@app.route('/descriptions', methods=['POST'])
def descriptions():
	if request.method == 'POST':
		return insert_description(request.data)

def insert_description(description):
	required_fields = ['track_id', 'user_name', 'description']
	if not all([field in description for field in required_fields]):
		raise exceptions.ParseError()
	try:
		with queries.transaction():
			queries.enable_foreign_keys()
			queries.create_description(**description)
	except Exception as e:
		return { 'error' : str(e) }, status.HTTP_409_CONFLICT

	return description, status.HTTP_201_CREATED

if __name__ == "__main__":
	app.run()




