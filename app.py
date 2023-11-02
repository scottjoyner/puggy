from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection details (Update with your details)
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(user, password))

# Define the route to accept POST requests with the Cypher query
@app.route('/run-cypher', methods=['POST'])
def run_cypher():
    try:
        # Parse the incoming data to get the Cypher query
        data = request.get_json()
        query = data['query']

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
