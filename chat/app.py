from flask import Flask, request, jsonify
from database import db, ChatMessage
from chatbot_service import get_chatbot_response
from flask_httpauth import HTTPBasicAuth
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db.init_app(app)
auth = HTTPBasicAuth()

# Basic user authentication setup
users = {
    "admin": "password",
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/api/message/send', methods=['POST'])
@auth.login_required
def send_message():
    data = request.json
    user_id = data.get('userId')
    message = data.get('message')

    try:
        response_message = get_chatbot_response(message)
        new_message = ChatMessage(user_id=user_id, text=message, sender='user')
        new_response = ChatMessage(user_id=user_id, text=response_message, sender='bot')
        db.session.add(new_message)
        db.session.add(new_response)
        db.session.commit()
        return jsonify({"reply": response_message}), 200
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/chat/history', methods=['GET'])
@auth.login_required
def fetch_chat_history():
    user_id = request.args.get('userId')

    try:
        messages = ChatMessage.query.filter_by(user_id=user_id).all()
        return jsonify([msg.serialize() for msg in messages]), 200
    except Exception as e:
        logging.error(f"Error fetching chat history: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/chat/start', methods=['POST'])
@auth.login_required
def start_chat():
    data = request.json
    user_id = data.get('userId')

    try:
        # Logic to handle starting a new chat session
        return jsonify({"message": "Chat session started"}), 200
    except Exception as e:
        logging.error(f"Error starting chat: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)

