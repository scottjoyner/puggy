from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.Column(db.String(10), nullable=False) # 'user' or 'bot'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
            "sender": self.sender
        }

