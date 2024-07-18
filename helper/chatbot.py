import json
import random
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop_words
from spacy.lang.en.stop_words import STOP_WORDS as en_stop_words
from spacy.tokens import Doc
from langdetect import detect
import re

# Load questions and answers from the JSON file
def load_qa(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        qa_data = json.load(file)
    return qa_data

# Load French and English spaCy models
nlp_fr = spacy.load('fr_core_news_md')
nlp_en = spacy.load('en_core_web_md')

# Preprocess text based on the specified language
def preprocess_text(text, language):
    if language == 'fr':
        doc = nlp_fr(text.lower())
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space and token.text not in fr_stop_words]
    elif language == 'en':
        doc = nlp_en(text.lower())
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space and token.text not in en_stop_words]
    else:
        doc = nlp_fr(text.lower())  # Default to French if language is not supported
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space and token.text not in fr_stop_words]
    
    return ' '.join(tokens)
# Extract keywords from intents.json for custom spell checking
def extract_keywords_from_intents(qa_data, lang):
    keywords = []
    for intent in qa_data['intents']:
        if 'patterns' in intent and lang in intent['patterns']:
            keywords.extend(intent['patterns'][lang])
    return set(keywords)




def custom_spell_checker(input_text, keywords, spell_checker):
    words = input_text.split()
    corrected_words = []
    for word in words:
        if word in keywords:
            corrected_words.append(word)
        else:
            corrected_words.append(spell_checker.correction(word))
    return ' '.join(corrected_words)
# Find the closest question to the user input
def get_closest_question(user_input, questions, language):
    best_similarity = 0.0
    closest_question = None

    user_input_processed = preprocess_text(user_input, language)

    for question in questions:
        question_processed = preprocess_text(question, language)
        if language == 'fr':
            similarity = nlp_fr(user_input_processed).similarity(nlp_fr(question_processed))
        elif language == 'en':
            similarity = nlp_en(user_input_processed).similarity(nlp_en(question_processed))
        else:
            continue  # Skip if language is unsupported
        
        if similarity > best_similarity:
            best_similarity = similarity
            closest_question = question
    
    return closest_question

# Function to split the message into parts
def split_message(message):
    separators = r'[.,;!?&|]|\bet\b|\bou\b|\band\b|\bor\b'  # Separators and keywords for splitting
    parts = re.split(separators, message)
    parts = [part.strip() for part in parts if part.strip()]
    return parts

# Function to process each part of the message and generate a response
def chatbot_logic(user_input, qa_data, language):
   
    message = user_input.lower()
    print("message",message)
    # Split the message into parts
    parts = split_message(message)

    responses = []
    
    for part in parts:
       
        # Reset lists for each part of the message
        questions = []
        question_answer_map = {}

        # Extract questions and corresponding answers from QA data
        for intent in qa_data["intents"]:
            if language in intent["patterns"]:
                for pattern in intent["patterns"][language]:
                    questions.append(pattern)
                    question_answer_map.setdefault(pattern, set()).update(intent["responses"][language])

        # Find the closest question for this part
        closest_question = get_closest_question(part, questions, language)
        if closest_question:
            response = random.choice(list(question_answer_map[closest_question]))  # Random selection among unique responses
            responses.append(response)       
        else:
            if language == 'fr':
                responses.append("Désolé, je ne comprends pas cette question")
            elif language == 'en':
                responses.append("Sorry, I don't understand this question")
            else:
                responses.append("Sorry, I don't understand this question")
    
    # Concatenate all responses into a single string
    answer = ' '.join(responses)
    print("answer",answer)
    return answer
