import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
from bson.json_util import dumps
import json
from dotenv import load_dotenv
load_dotenv()
import os
ADDRESS = os.getenv("address")
USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
client = pymongo.MongoClient("mongodb+srv://"+ USERNAME + ":" + PASSWORD + "@" + ADDRESS + "?retryWrites=true") 
db = client.kotijutut
collection = db.TVShows

CORS(app)

# Check if program works well
@app.route('/ping', methods=['GET'])
def ping_pong():
	return jsonify('pong!')


@app.route('/shows', methods=['GET', 'POST'])
def all_shows():
	col_results = json.loads(dumps(collection.find()))
	response_object = {'status': 'success'}
	if request.method == 'POST':
		post_data = request.get_json()
		collection.insert_one(post_data);
		response_object['message'] = 'Show added!'
	else:
		response_object['shows'] = col_results
	return jsonify(response_object)


@app.route('/shows/<show_id>', methods=['PUT', 'DELETE'])
def single_show(show_id):
	response_object = {'status': 'success'}
	if request.method == 'PUT':
		post_data = request.get_json()
		myquery = { "id": show_id }
		newvalues = { "$set": post_data }
		print(newvalues, myquery)
		collection.update_one(myquery, newvalues)
		response_object['message'] = 'Show updated!'
	if request.method == 'DELETE':
		myquery = { "id": show_id }
		collection.delete_one(myquery)		
		response_object['message'] = 'Show removed!'
	return jsonify(response_object)


if __name__ == '__main__':
	app.run()
