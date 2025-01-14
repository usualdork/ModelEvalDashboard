# app.py
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from hugchat import hugchat
from hugchat.login import Login
from flask_session import Session
from functools import wraps
import os
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configure Flask-Session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Thread pool for handling multiple model requests
executor = ThreadPoolExecutor(max_workers=4)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'cookies' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_model_response(cookies, model_index, prompt, response_length):
    try:
        chatbot = hugchat.ChatBot(cookies=cookies)
        chatbot.switch_llm(model_index)
        
        length_params = {
            "short": {"max_length": 100},
            "medium": {"max_length": 300},
            "detailed": {"max_length": 1000}
        }
        
        response = chatbot.chat(
            prompt,
            **length_params.get(response_length, {"max_length": 300})
        ).wait_until_done()
        
        return {'success': True, 'response': response}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        sign = Login(email, password)
        cookies = sign.login()
        
        if cookies:
            # Store cookies in session
            session['cookies'] = cookies.get_dict()
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'error': 'Login failed'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
@login_required
def get_models():
    try:
        chatbot = hugchat.ChatBot(cookies=session['cookies'])
        models = chatbot.get_available_llm_models()
        return jsonify({'models': models})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
@login_required
def generate_responses():
    try:
        data = request.json
        prompt = data.get('prompt')
        selected_models = data.get('models', [])
        response_length = data.get('responseLength', 'medium')
        
        if not prompt or not selected_models:
            return jsonify({'error': 'Prompt and selected models are required'}), 400
            
        futures = []
        for model_index in selected_models:
            future = executor.submit(
                get_model_response,
                session['cookies'],
                model_index,
                prompt,
                response_length
            )
            futures.append((model_index, future))
            
        responses = {}
        for model_index, future in futures:
            result = future.result()
            if result['success']:
                responses[str(model_index)] = result['response']
            else:
                responses[str(model_index)] = f"Error: {result['error']}"
                
        return jsonify({'responses': responses})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

if __name__ == '__main__':
    app.run(debug=True)
