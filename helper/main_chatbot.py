
from flask_cors import CORS
from flask import Flask, request, jsonify
from chatbot import chatbot_logic, load_qa
from json_modifier import replace_json_file  
import json

app = Flask(__name__)
CORS(app)
# File path for the intents JSON file
file_path = "intents.json"

# Load initial QA data from the JSON file
qa_data = load_qa(file_path)


# Route to modify the JSON file with a new file
@app.route('/modify_json', methods=['POST'])
def handle_modify_json():
    global qa_data
    new_file_path = request.json.get('new_file_path')
    
    # Check if new_file_path is provided; if not, return a 400 error response
    if not new_file_path:
        return jsonify({"success": False, "message": "No new_file_path provided"}), 400
    
    # Replace the existing JSON file with the new file
    success, message = replace_json_file(file_path, new_file_path)
    
    if success:
        # Reload QA data after modification
        qa_data = load_qa(file_path)
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "message": message}), 500
    

# Route for the chatbot logic
@app.route('/chatbot', methods=['POST'])
def handle_chatbot():
    if request.method == 'POST':
        user_input = request.json['message']
        langue = request.args.get('langue')
        # Call chatbot logic function to get response
        answer = chatbot_logic(user_input, qa_data,langue)
        
        response = {
            "message": answer, # Create a response dictionary with the chatbot's answer
            
        }
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True ,host='0.0.0.0')
