from flask_cors import CORS
from flask import Flask, request, jsonify
from chatbot_client import load_qa,chatbot_logic
import json
from action_client import handle_user_input,extract_user_data
import requests
from action_client import fetch_external_api_data
app = Flask(__name__)
CORS(app)
# File path for the intents JSON file
file_path = "tag.json"

# Load initial QA data from the JSON file
qa_data = load_qa(file_path)

"""
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
 """   

    

"""# Route for the chatbot logic
def fetch_external_api_data():
    external_api_url = "https://pp-unum-back.etcinfo.tech/api/societe/clients?"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MTk5MDgyNTMsImV4cCI6MTcxOTk0NDI1Mywicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.tXykwlGVtKd1e0X1OLigXjNMHcMlUsljdsIjfEppv5JCcfPrlnxi81IT64E4xAD3oBA4W8_mN-B1H4LlZxO9y4ZQe-7lfAlKOsWZkzuVkSDxKNog--tstLguVZqxgmoe0P0jjg7fuyMSQSJHT-UeKG17LhzgWut-4Ixsjg6BiuqpatuNwCK4b0NHzdXqtqO_YcILviPC2Y3M8YxYD0A7Lzz9JUr4gw1RM-LW7ap6V2ZG4W1XOBGJRQzD2_VlAXdy1-3G6j3BgJHYbUrwCOeVZwgei66yxt7bKvNFR9HjteH1H89EAtCcCU7D34xlmi8RLWv456KHXcBf8tI8Vd3Nwg"
    }
   
    try:
        response = requests.get(external_api_url, headers=headers)
        print(f"Status Code: {response.status_code}")  # Debugging line
        print(f"Response Content: {response.content}")  # Debugging line
        
        if response.status_code == 200:
            return response.json().get('hydra:member')
        else:
            return {"error": f"Failed to fetch data from external API, status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
"""




"""# Route for the chatbot logic
@app.route('/gestion', methods=['POST'])
def handle_chatbot():
    if request.method == 'POST':
        user_input = request.json['message']
        langue = request.args.get('langue')
        qa_data = 'tag.json'
        json_filename = 'client.json'
        
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401
        
        #external_data =fetch_external_api_data()
        # Call chatbot logic function to get response
        response, extracted_data = handle_user_input(user_input, qa_data, json_filename, static_token=auth_header,  language='fr')
        return jsonify({"response": response,
                        "extracted_data": extracted_data,
                        #"external_data": external_data
                        #"auth_header": auth_header
                        })
      
        # Extract and respond function call
       # reponse = extract_and_respond(user_input)
        
        # Prepare the response JSON
        response = {
            "message": answer,
            "tags": tag,
            "reponse": reponse
        }
        
        # Add user input and response to JSON file
        json_filename = "client.json"
        if add_user_input_to_json(user_input, json_filename):
            print(f"Réponse ajoutée avec succès dans {json_filename}")
        else:
            print(f"Erreur lors de l'ajout de la réponse dans {json_filename}")
        
        # Return the JSON response to the client
        return jsonify(response) 
     """   





# Route for the chatbot logic
@app.route('/gestion', methods=['POST'])
def handle_chatbot():
    if request.method == 'POST':
        user_input = request.json['message']
        langue = request.args.get('langue')
        qa_data = 'tag.json'
        json_filename = 'client.json'
        
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401
        
        #external_data =fetch_external_api_data()
        # Call chatbot logic function to get response
        response, extracted_data = extract_user_data(user_input)
        return jsonify({"response": response,
                        "extracted_data": extracted_data,
                        #"external_data": external_data
                        #"auth_header": auth_header
                        })     
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    











