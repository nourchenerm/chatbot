import spacy
import re
import requests
from user_data import payload
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop_words
from spacy.lang.en.stop_words import STOP_WORDS as en_stop_words


def extract_clients_info(url,code_client, token):
    headers = {
        'Authorization': f'Bearer {token}'  # Insérez ici votre méthode d'authentification et token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Gère les erreurs HTTP
        clients = response.json()['hydra:member']  # Accès aux membres de la réponse JSON
       
        filtered_clients = []
        
        for client in clients:
            if 'code' in client:
                if  client['code'].lower() == code_client[0].lower():
                       
                        for adresse in client['adresses']:  
                                mode_reglement_id = None
                                regime_tva_id = None
                                forme_juridique_id = None
                                if client.get('modeReglement') and client['modeReglement'].get('id'):
                                       mode_reglement_id = client['modeReglement'].get('id')  
                                if client.get('formeJuridique') and client['formeJuridique'].get('id'):
                                       forme_juridique_id = client['formeJuridique'].get('id')  
                                if client.get('regimeTva') and client['regimeTva'].get('@id'):
                                       regime_tva_id =  client['regimeTva'].get('@id').split('/')[-1]        
                                       
                                client_data = {
                                    'idTier': client.get('id'),
                                    'nom': client.get('nom'),
                                    'adresse': adresse.get('adresse'),
                                    'code': client.get('code'),
                                    'email': client.get('email'),
                                    'modeReglement' : mode_reglement_id,
                                    'siteWeb': client.get('siteWeb'),
                                    'telephone': client.get('telephone'),
                                    'baseCalcul':client.get('baseCalcul'),
                                    'numeroTva':client.get('numeroTva'),
                                    'formeJuridique': forme_juridique_id,
                                    'regimeTva': regime_tva_id,
                                    'regimeTvaId': regime_tva_id,    
                                }
                                filtered_client_data = {k: v for k, v in client_data.items() if v is not None}
                                filtered_clients.append(filtered_client_data)
        return filtered_clients

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {str(e)}")
        return []
    

def extract_contact_info(client_id, token):
    url = f"https://pp-unum-back.etcinfo.tech/api/societe/clients/{client_id}/contact"
    print(url)  # URL de votre API pour obtenir les contacts du client
    headers = {
        'Authorization': f'Bearer {token}'  # Insérez ici votre méthode d'authentification et token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Gère les erreurs HTTP
        contact_info = response.json()
        contact = response.json()['hydra:member']  # Accès aux données de contact de la réponse JSON
       # print("contact",contact)
        # Vérifiez si la réponse contient un identifiant de contact
        if contact:
            contact_id = contact[0].get('id')  # Prend le premier contact et extrait l'ID
            return contact_id
        else:
            print("L'ID du contact n'a pas été trouvé dans la réponse.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {str(e)}")
        return None
def extract_article_id(url,article_code, token):
    print(url) 
    headers = {
        'Authorization': f'Bearer {token}' 
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Gère les erreurs HTTP
        article_info = response.json()
        articles = response.json()['hydra:member']  # Accès aux données de article de la réponse JSON
      
        # Vérifiez si la réponse contient un identifiant de article
        for article in articles:
             if  article['reference'].lower() == article_code.lower():  # Check if the code matches
                return article.get('id')  # Return the associated article ID
        
        print("L'article avec le code spécifié n'a pas été trouvé.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {str(e)}")
        return None
    
def extract_article_info(url,article_id, token):

 

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload1 = {
    "articleId": article_id,
    "typePiece": "ventes",
    "tierId": 37,
    "baseCalcul": "HT",
    "quantity": 1,
    "regimeTvaId": 5,
    "estAssujetiTpf": False
    }   
    #print("Payload:", payload)

    try:
        response = requests.post(url, headers=headers, json=payload1)
        response.raise_for_status()  # Gère les erreurs HTTP

        article_obj= response.json()
        print("article" ,article_obj)
        article =  {
                    "id": 0,
                    "articleId": article_obj["articleId"],
                    "code": article_obj["code"],
                    "description": article_obj["description"],
                    "lotSerie": "Aucun",
                    "quantity": 1,
                    "prixUnitaireHTVente": article_obj["prixUnitaireHTVente"],
                    "prixUnitaireTTCVente": article_obj["prixUnitaireTTCVente"],
                    "prixUnitaireHTAchat": article_obj["prixUnitaireHTAchat"],
                    "prixTotalHT": article_obj["prixTotalHT"],
                    "prixUnitaireTTCAchat": article_obj["prixUnitaireTTCAchat"],
                    "prixTotalTTC": article_obj["prixTotalTTC"],
                    "tva": article_obj["tva"]["id"],
                    "tpf": article_obj["tpf"]["id"],
                    "unite": article_obj["unite"]["id"],
                    "poidsUnitaireBrut": article_obj.get("poidsUnitaireBrut", 0),
                    "poidsTotalBrut": article_obj.get("poidsTotalBrut", 0),
                    "poidsUnitaireNet": article_obj.get("poidsUnitaireNet", 0),
                    "poidsTotalNet": article_obj.get("poidsTotalNet", 0),
                    "tauxRemise": 0,
                    "qteParColis": article_obj.get("qteParColis", 1),
                    "montantTva": article_obj["prixUnitaireTTCVente"] - article_obj["prixUnitaireHTVente"],
                    "montantRemiseHT": 0,
                    "montantRemiseTTC": 0,
                    "nbrColis": 1,
                    "montantTPF": 0,
                    "level": "1",
                    "mode": "update",
                    "isShow": False,
                    "lastParamsChange": "",
                    "articlesComposants": [],
                    "remises": [],
                    "tarifArticles": [],
                    "estCommentaire": False,
                    "estSousTotal": False,
                    "uniteId": article_obj["unite"]["id"],
                    "tvaId": article_obj["tva"]["id"],
                    "tpfId": article_obj["tpf"]["id"],
                    "ecoParticipationTotalTTC": 0,
                    "uniteColis": 0,
                    "valeurTPF": 0,
                    "valeurRemise": 0
                }
        payload['articles'].append(article)
        
        ligne_data = {
            "id": 0,  
            "articleId": article_obj["articleId"],
            "code": article_obj["code"],
            "description": article_obj["description"],
            "quantity": 1, 
            "lotSerie": 0,  
            "prixUnitaireHTVente": article_obj["prixUnitaireHTVente"],
            "prixUnitaireTTCVente": article_obj["prixUnitaireTTCVente"],
            "prixUnitaireHTAchat": article_obj["prixUnitaireHTAchat"],
            "tauxRemise": 0,  
            "montantRemiseHT": 0, 
            "montantRemiseTTC": 0, 
            "montantTPF": 0,  
            "montantTva": article_obj["prixUnitaireTTCVente"] - article_obj["prixUnitaireHTVente"], 
            "nbrColis": 1,  
            "qteParColis": article_obj["qteParColis"],
            "poidsTotalBrut": article_obj["poidsTotalBrut"] * 1,  
            "poidsTotalNet": article_obj["poidsTotalNet"] * 1,  
            "poidsUnitaireBrut": article_obj["poidsUnitaireBrut"],
            "poidsUnitaireNet": article_obj["poidsUnitaireNet"],
            "prixTotalHT": article_obj["prixTotalHT"] * 1,  
            "prixTotalTTC": article_obj["prixTotalTTC"] * 1, 
            "tauxTPF": 0,  
            "valeurTPF": 0,  
            "estCommentaire": False,
            "estSousTotal": False,
            "ordre": 7,  
            "tauxTva": article_obj["tauxTva"],
            #"prixAchatHT": article_obj["prixAchatHT"],
            "valeurRemise": 0,  
            "unite": int(article_obj["unite"]["id"]),
            "uniteColis": 0,  
            "tva": article_obj["tva"]["id"],
            "tpf": article_obj["tpf"]["id"],
            "sousTotalPrixHT": 0,  
            "sousValeurTva": (article_obj["prixUnitaireTTCVente"] - article_obj["prixUnitaireHTVente"]) * (article_obj["tva"]["valeur"] / 100)
        }
        #print("ligne_data",ligne_data)
        return ligne_data 

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {str(e)}")
        return None
def extract_total_amount(url,payload,token):
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    #print("Payload:", payload)
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Gère les erreurs HTTP

        total_info = response.json()
        print("Total Info:", total_info)  # Affiche les informations totales
        pied = {
        "totalHt": total_info.get("totalHt", 0),
        "totalTva": total_info.get("totalTva", 0),
        "totalTTC": total_info.get("totalTTC", 0),
        "remiseGlobalHt": total_info.get("remiseGlobalHt", 0),
        "tauxRemiseGlobal": total_info.get("tauxRemiseGlobal", 0),
        "remiseGlobalTtc": total_info.get("remiseGlobalTtc", 0),
        "brutHt": total_info.get("brutHt", 0),
        "soldeDu": total_info.get("totalTTC", 0),
        "montantRegle": total_info.get("montantRegle", 0),
        "totalQuantity": total_info.get("totalQuantity", 0),
        "totalEcoParticipation": total_info.get("totalEcoParticipation", 0),
        "totalPoidsNet": total_info.get("totalPoidsNet", 0),
        "totalPoidsBrut": total_info.get("totalPoidsBrut", 0),
        "totalColis": total_info.get("totalColis", 0),
        "totalTPF": total_info.get("totalTPF", 0)
    }

        return pied
    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP: {http_err}")
        print(f"Contenu de la réponse: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erreur lors de la requête API: {str(req_err)}")
    return None
def extract_prefixe(url,token):
    
    print(url) 
    headers = {
        'Authorization': f'Bearer {token}' 
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Gère les erreurs HTTP
        prefixe = response.json()
        return prefixe
      

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {str(e)}")
        return None

def check_stock(article_id, quantity, api_url, token):
   
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "articleId": article_id,
        "quantity": str(quantity)  # Convertir en chaîne si nécessaire
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        return True  # Mise à jour réussie
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API: {e}")
        return False    