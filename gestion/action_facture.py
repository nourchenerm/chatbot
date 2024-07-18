import spacy
import re
import requests
from user_data import facture_data,config
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop_words
from spacy.lang.en.stop_words import STOP_WORDS as en_stop_words



nlp_fr = spacy.load('fr_core_news_md')  # Charger le modèle français de spaCy
nlp_en = spacy.load('en_core_web_md')

def custom_spell_checker1(input_text, keywords, spell_checker):
    words = input_text.split()
    corrected_words = []
    for word in words:
        # Only check spelling for keywords
        if word in keywords:
            corrected_words.append(word)
        else:
            # Check if the word is a keyword, if not, leave it unchanged
            correction = spell_checker.correction(word)
            if correction and correction in keywords:  # Only replace if correction is a valid keyword
                corrected_words.append(correction)
            else:
                corrected_words.append(word)  # Keep the original word if no correction is valid
    return ' '.join(corrected_words)
def add_facture(facture_data, api_url, static_token):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {static_token}"
    }
    

    response = requests.post(api_url, json=facture_data
    , headers=headers)
        
    if response.status_code == 200:
            print("facture ajouté avec succès.")
            return True
            # Gérer d'autres actions en cas de succès, si nécessaire
    else:
            print(f"Erreur lors de l'ajout de facture: {response.status_code}")
            print(f"Message d'erreur : {response.json()}")
            return False
    
 
def extract_article_codes(message):
    # Utiliser une expression régulière pour trouver tous les codes article qui commencent par 'art'
    pattern = r'art\d+'
    codes = re.findall(pattern, message)
    return codes    
def extract_article_quantity(message):
    # Utiliser une expression régulière pour trouver tous les codes article qui commencent par 'art'
    pattern = r'quantity\d+'
    codes = re.findall(pattern, message)
    return codes    



def extract_client_codes(message):
    # Utiliser une expression régulière pour trouver tous les codes qui commencent par 'cli'
    pattern = r'cli\d+'
    codes = re.findall(pattern, message)
    return codes

# Fonction pour détecter l'information dans le message utilisateur
def detect_information(user_input):
    user_input_lower = user_input.lower()
    detected_info = {}
    values_client = ["referenceChez", "articles", "datePiece", "dateCommande", "numeroCommande", "numero", "status", "codeStatus", "dateLivraison", "remiseGlobal"]
    
    # Mot-clés et leurs alias
    facture_keywords = {
        'tier.nom': ['nom'],
        'tier.code': ['code client'],
        'ligne.articleId': ['code article'],
        'ligne.quantity': ['quantite'],
        'referenceChez': ['referenceChez', 'référence chez', 'réf chez'],
        'articles': ['articles', 'produits', 'items'],
        'datePiece': ['datePiece', 'date pièce', 'date de la pièce'],
        'dateCommande': ['dateCommande', 'date commande', 'date de la commande'],
        'numeroCommande': ['numeroCommande', 'numéro commande', 'numéro de commande'],
        'numero': ['numero', 'numéro'],
        'dateLivraison': ['dateLivraison', 'date livraison'],
    }
    
    # Extraire toutes les quantités et articles
    quantities = extract_value(user_input_lower, 'quantite')
    articles = extract_value(user_input_lower, 'code_article')
    
    # Détection des informations
    for key, aliases in facture_keywords.items():
        for alias in aliases:
            if alias in user_input_lower:
                print(alias)
                value = extract_value(user_input_lower, alias)
                if value:
                    if key not in detected_info:
                        detected_info[key] = []
                    detected_info[key] = value

    # Ajout des quantités et articles
    if quantities:
        detected_info['ligne.quantity'] = quantities
    if articles:
        detected_info['ligne.articleId'] = articles
    
    # Traitement des valeurs détectées
    if detected_info:
        for key, values in detected_info.items():
            if key in config and isinstance(config[key], tuple) and len(config[key]) > 2:
                for value in values:
                    if value in config[key][2]:
                        facture_data[key] = config[key][2][value]
            elif key in values_client and key not in config:
                facture_data[key] = values[0]
                

        return detected_info

    return None


# Fonction pour trouver la clé la plus proche par similarité
def get_closest_cle(user_input, keywords):
    threshold=0.7
    best_similarity = 0.0
    closest_question = None

    user_input_doc = nlp_fr(user_input)

    # Comparaison de similarité pour chaque mot-clé
    for question in keywords.keys():
        question_doc = nlp_fr(question)
        similarity = user_input_doc.similarity(question_doc)
        if similarity > best_similarity:
            best_similarity = similarity
            closest_question = question

    # Retourner le mot-clé le plus similaire si la similarité dépasse le seuil
    if best_similarity >= threshold:
        return closest_question
    else:
        return None

# Fonction pour extraire la valeur après un mot-clé dans le message utilisateur
def extract_value(message, keyword):
    # Regex pour extraire toutes les valeurs après le mot-clé
    pattern = rf'{keyword}\s+(\d{{2}}/\d{{2}}/\d{{4}}|\d+|[^\s]+)'  # Capturer un nombre ou un mot non suivi d'un espace
    values = re.findall(pattern, message)
    return values


def preprocess_text(text, language):
    if language == 'fr':
        doc = nlp_fr(text.lower())
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space and not (token.is_stop and token.text not in ['etc'])]
    elif language == 'en':
        doc = nlp_en(text.lower())
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space and not token.is_stop]
    else:
        doc = nlp_fr(text.lower())  # Default to French if language is not supported
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space and not (token.is_stop and token.text not in ['etc'])]
    
    return ' '.join(tokens)

def ajouter_option(champ, option):
    token, api_url, options = config[champ]
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {token}"
    }
    url = f"{api_url}?type={option}"  # Correction ici pour concaténer correctement l'URL avec l'option
    payload = {
            "@id": "/api/societe/{champ}",
            "@type": champ,
            "libelle": option,
            "estPredefini": True,
            "estDefault": False,
            "estDesactive": False
    }
        
    try:
        response = requests.post(url, json=payload, headers=headers)  # Utilisation de `url` au lieu de `api_url` ici
        if response.status_code == 201:
            print(f"Nouvelle option '{option}' ajoutée avec succès à la plateforme.")
            print(f"Réponse de l'API : {response.json()}")
          
            return response.json().get('id')
        else:
            print(f"Erreur lors de l'ajout de l'option '{option}' à la plateforme: {response.status_code}")
            print(f"Message d'erreur : {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête lors de l'ajout de l'option '{option}' à la plateforme: {str(e)}")

