import datetime
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# Get all messages
@app.route('/messages', methods=['GET'])
def get_all_messages():
    messages = Message.query.order_by(Message.created_at).all()
    messages_serialized = [message.to_dict() for message in messages]
    return jsonify(messages_serialized), 200

# Update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()
    message = Message.query.get(id)
    if message:
        message.body = data['body']
        message.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(message.to_dict()), 200
    else:
        return jsonify({'message': 'Message not found'}), 404

# Delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    else:
        return jsonify({'message': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
