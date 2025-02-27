from flask import Blueprint, jsonify, render_template, request, session as flask_session
from .models import ChatSession, Message

app = Blueprint('app', __name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Create a new session
@app.route('/session/create/', methods=['POST'])
def create_session():
    chat_session = ChatSession()
    flask_session['session_id'] = chat_session.session_id  # Only when creating a new chat
    chat_session.save()
    return render_template('session_detail.html', session_id=chat_session.session_id)


@app.route('/session/<session_id>/', methods=['GET'])
def session_detail(session_id):
    session = session_id

    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    # Get all messages related to this session
    messages = session.messages.all()
    
    return render_template('session_detail.html', session= session,messages= messages,session_id = session_id)

@app.route('/generate_response/', methods=['POST'])
def generate_response():
    data = request.json
    user_input = data.get('user_input')
    print(user_input)
    session_id = flask_session.get('session_id')
    message = Message(session_id=session_id, prompt=user_input)
    message.generate_completion()

    # Save prompt tokens
    message.prompt_tokens = len(user_input.split())

    message.save()

    return jsonify({'response': message.completion})


@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    # Clear the cache
    return jsonify({'message': 'Cache cleared.'})

@app.route('/get_sessions', methods=['GET'])
def get_sessions():
    # Get all sessions
    sessions = ChatSession.get_all_sessions()
    return jsonify(sessions)