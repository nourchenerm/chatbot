from flask_cors import CORS
from flask import Flask, request, jsonify
from chatbot import chatbot_logic, load_qa,custom_spell_checker,extract_keywords_from_intents
from spellchecker import SpellChecker
from autocorrect import Speller

app = Flask(__name__)
CORS(app)

# File path for the intents JSON file
file_path1 = "intents.json"

# Load initial QA data from the JSON file
qa_data = load_qa(file_path1)

# Initialize the spell checkers
spell_fr = SpellChecker(language='fr')
spell_en = Speller(lang='en')

keywords_fr = extract_keywords_from_intents(qa_data, 'fr')
keywords_en = extract_keywords_from_intents(qa_data, 'en')



# Route for the chatbot logic
@app.route('/chatbot', methods=['POST'])
def handle_chatbot():
    if request.method == 'POST':
        user_input = request.json['message']
        langue = request.args.get('langue')
        
        if langue == 'fr':
            corrected_input = custom_spell_checker(user_input, keywords_fr, spell_fr)
            print("corrected_input:", corrected_input)
        else:
            corrected_input = custom_spell_checker(user_input, keywords_en, spell_en)
            print("corrected_input:", corrected_input)

        # Call chatbot logic function to get response
        answer = chatbot_logic(corrected_input, qa_data, langue)
        
        response = {
            "message": answer,  # Create a response dictionary with the chatbot's answer
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
