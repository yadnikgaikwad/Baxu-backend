from flask import Blueprint, jsonify, request
import openai
import os
import uuid
from datetime import datetime
import time
import requests

chat_bp = Blueprint('chat', __name__)

# This in-memory store holds conversation history for each user.
# In a production environment, consider using a persistent store like Redis, a database, or a dedicated conversation management service
# to ensure conversations persist across server restarts and scale for multiple users.
conversation_store = {}

# Function to load the system prompt for the AI agent.
# This is where you can define the AI's persona, knowledge, and interaction guidelines.
# The content of this prompt is crucial for shaping the AI's responses and brand voice.
# You can update the content of the `system_prompt.txt` file to change the AI's behavior.
# For this demo, the system prompt is loaded from a file, but in a real application, it might be fetched from a database or configuration service.
def load_system_prompt():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, "system_prompt.txt")
        print("Looking for system_prompt.txt at:", prompt_path)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("system_prompt.txt file not found. Please ensure the file exists in the correct directory.")
        return "[System prompt not found]"


@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({"error": "Message is required", "status": "error"}), 400

    # Load system prompt
    system_prompt = load_system_prompt()

    # OpenAI API setup
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    if not openai_api_key:
        return jsonify({"error": "OPENAI_API_KEY not set", "status": "error"}), 500

    try:
        openai.api_key = openai_api_key
        openai.api_base = openai_api_base
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or "gpt-3.5-turbo" if you don't have access to gpt-4o
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=300,
        )
        ai_message = response.choices[0].message['content'].strip()
        return jsonify({
            "response": ai_message,
            "conversation_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success"
        })
    except Exception as e:
        import traceback
        print("OpenAI API error:", e)
        traceback.print_exc()
        return jsonify({"error": "AI service unavailable", "status": "error"}), 503

