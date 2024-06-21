import spacy
import re
import json

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

def extraire_donnees(message):
    # Initialiser les variables pour les données à extraire
    nom = None
    prenom = None
    age = None

    # Utiliser des expressions régulières pour trouver le nom, le prénom et l'âge
    nom_match = re.search(r'\bnom\s+(?:est\s+|)\s*(\w+)', message, re.IGNORECASE)
    prenom_match = re.search(r'\bprénom\s+(?:est\s+|)\s*(\w+)', message, re.IGNORECASE)
    age_match = re.search(r'(\d+)\s*(?:ans|âge)', message, re.IGNORECASE)

    if nom_match:
        nom = nom_match.group(1)
    if prenom_match:
        prenom = prenom_match.group(1)
    if age_match:
        age = age_match.group(1)

    # Créer un dictionnaire avec les données extraites
    donnees_client = {
        "nom": nom,
        "prenom": prenom,
        "age": age
    }

    return donnees_client

# Exemple d'utilisation
message = "Ajouter un client, son nom est Talbi, prénom Rahma, et son âge est 24 ans."
donnees = extraire_donnees(message)
print(json.dumps(donnees, ensure_ascii=False))  # Convertir en JSON et imprimer

# Tests supplémentaires
messages = [
    "Ajouter un client, son prénom est Malek, son âge est 11 ans.",
    "Insérer un client, son nom est Martin, son âge est 45 ans.",
    "Création d'un client, le prénom est Sophie."
]

for msg in messages:
    donnees = extraire_donnees(msg)
    print(f"Message: {msg}")
    print(json.dumps(donnees, ensure_ascii=False))  # Convertir en JSON et imprimer
    print()
