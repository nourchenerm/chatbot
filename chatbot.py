import json
import difflib
import random
from langdetect import detect

# Load questions and answers from the JSON file
def load_qa(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        qa_data = json.load(file)
    return qa_data

# Find the closest matching question
def get_closest_question(user_input, questions):
    closest_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.6)
    if closest_match:
        return closest_match[0]
    else:
        return None

# Process user input and generate a response
def chatbot_logic(user_input, qa_data):
    try:
        language = detect(user_input)
    except:
        language = 'fr'  # Default language
    
    questions = []
    question_answer_map = {}
    
    # Extract questions and corresponding answers from the QA data
    for intent in qa_data["intents"]:
        if language in intent["patterns"]:
            for pattern in intent["patterns"][language]:
                questions.append(pattern)
                question_answer_map[pattern] = intent["responses"][language]
    
    closest_question = get_closest_question(user_input, questions)
    if closest_question:
        answer = random.choice(question_answer_map[closest_question])
    else:
        if language == 'fr':
            answer = "Désolé, je ne comprends pas cette question"
        elif language == 'en':
            answer = "Sorry, I don't understand this question"
        else:
            answer = "Sorry, I don't understand this question"
    
    return answer


















"""
import json
import difflib
import random

from flask import jsonify

# Load questions and answers from the JSON file
def load_qa(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        qa_data = json.load(file)
    return qa_data


# Find the closest matching question
def get_closest_question(user_input, questions):
    closest_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.6)
    # Use difflib's get_close_matches to find the most similar question
    if closest_match:
        return closest_match[0]
    else:
        return None
    

# Process user input and generate a response
def chatbot_logic(user_input, qa_data):
    questions = []
    question_answer_map = {}
    
    # Extract questions and corresponding answers from the QA data
    for intent in qa_data["intents"]:
        for pattern in intent["patterns"]:
            questions.append(pattern)
            question_answer_map[pattern] = intent["responses"]
    
    closest_question = get_closest_question(user_input, questions)
    if closest_question:
        # If a close match to the user input is found, select a random response
        answer = random.choice(question_answer_map[closest_question])
    else:
        answer = "Désolé, je ne comprends pas cette question"
    
    return answer
"""























"""
from langdetect import detect
import json
import difflib
import random

from flask import jsonify

# Load questions and answers from the JSON file
def load_qa(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        qa_data = json.load(file)
    return qa_data


# Find the closest matching question
def get_closest_question(user_input, questions):
    closest_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.6)
    # Use difflib's get_close_matches to find the most similar question
    if closest_match:
        return closest_match[0]
    else:
        return None
    

# Process user input and generate a response
def chatbot_logic(user_input, qa_data):
    questions = []
    question_answer_map = {}
    
    # Extract questions and corresponding answers from the QA data
    for intent in qa_data["intents"]:
        for pattern in intent["patterns"]:
            questions.append(pattern)
            question_answer_map[pattern] = intent["responses"]
    
    closest_question = get_closest_question(user_input, questions)
    if closest_question:
        # If a close match to the user input is found, select a random response
        answer = random.choice(question_answer_map[closest_question])
    else:
        answer = "Désolé, je ne comprends pas cette question"
    
    return answer
"""