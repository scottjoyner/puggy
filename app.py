from flask import Flask, request, jsonify
from neo4j import GraphDatabase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

import configparser

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

config = configparser.ConfigParser()
config.read('puggy.ini')

# Neo4j connection details (Update with your details)
uri = config['neo4j']['uri']
user = config['neo4j']['username']
password = config['neo4j']['pwd']
driver = GraphDatabase.driver(uri, auth=(user, password))


# This is a simple example, replace with your database setup
users = {}

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']

    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    return jsonify({'success': True, 'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    hashed_password = users.get(username)

    if hashed_password and check_password_hash(hashed_password, password):
        return jsonify({'success': True, 'message': 'Login successful'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401



# Define the route to accept POST requests with the Cypher query
@app.route('/run-cypher', methods=['POST'])
def run_cypher():
    try:
        # Parse the incoming data to get the Cypher query
        data = request.get_json()
        query = data['query']
        print(query)
        # Function to execute the query
        def execute_query(tx, q):
            result = tx.run(q)
            return [record for record in result]

        # Run the query on the Neo4j database
        with driver.session() as session:
            result = session.write_transaction(execute_query, query)
            # Convert the result to a list of dictionaries
            return jsonify([dict(record) for record in result]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
