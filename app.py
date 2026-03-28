from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai # <--- Notice the new import here!
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# The new Google GenAI client automatically looks for the GEMINI_API_KEY in your .env file
client = genai.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/authenticate', methods=['POST'])
def authenticate_ticket():
    data = request.json
    qr_text = data.get('qr_text', '')
    target_date = data.get('target_date', '')

    prompt = f"""
    QR Data: "{qr_text}"
    Target Date: "{target_date}"
    Extract the date from the QR and compare it to the target date. 
    Return STRICTLY JSON format: {{"is_valid": true/false, "reason": "brief explanation"}}
    """

    try:
        # The new way to ask the AI
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        print("AI SAID:", response.text)
        
        # Clean the response in case AI adds markdown
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return jsonify(json.loads(clean_json))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)