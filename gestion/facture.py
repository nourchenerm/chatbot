from flask import Flask, request, jsonify, session
from flask_cors import CORS
import secrets
import numpy
from chatbot_client import load_qa, closest_tag,chatbot_logic
from action_facture import preprocess_text, add_facture, detect_information, ajouter_option,custom_spell_checker1
from extract_info import extract_clients_info,extract_contact_info,extract_article_info,extract_article_id,extract_total_amount,extract_prefixe,check_stock
from user_data import config, facture_data, facture_keywords,payload,values_key
from spellchecker import SpellChecker

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secret key for sessions
CORS(app)
spell_fr = SpellChecker(language='fr')

# File path for the intents JSON file
file_path = "tag.json"

# Load initial QA data from the JSON file
qa_data = load_qa(file_path)



@app.route('/facture', methods=['POST'])
def chatbot():
    message = request.json['message']
    input = preprocess_text(message, "fr")
    user_input = custom_spell_checker1(input, values_key, spell_fr)
    print("corrected_input:", user_input)
    articles = []
    des_article = {}
    
    # Retrieve session context or initialize it
    context = session.get('context', 'initial')
    pending_additions = session.get('pending_additions', {})
    tag1 = closest_tag(user_input, qa_data, "fr")
    clients = []
    if context == 'initial' and tag1 != 'confirmer' and tag1 != 'oui' and tag1 != 'non'  :
        detected_info = detect_information(user_input)
        print("vhb dvnl:,kml,;m," ,detected_info)
        prefixe = extract_prefixe("https://pp-unum-back.etcinfo.tech/api/societe/numerotations/generate-prefix?type=facture",token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
        print("prefixe",prefixe)
        facture_data['numero'] = prefixe
        if detected_info:
                nom_client = detected_info.get('tier.nom') 
                print("nom",nom_client)
                code_client = detected_info.get('tier.code')
                print("code_client",code_client)
                quantity = detected_info.get('ligne.quantity')
                print("quantity",quantity)
                codes =detected_info.get('ligne.articleId')
                print("codes",codes)
                if quantity != None:
                    max_length = max(len(codes), len(quantity))

                    # Boucle pour construire le dictionnaire
                    for i in range(max_length):
                        article_id = codes[i] if i < len(codes) else None
                        quantite = quantity[i] if i < len(quantity) else '1'  # Valeur par défaut 1

                        if article_id:  # Assurez-vous que l'ID de l'article n'est pas None
                            des_article[article_id] = quantite
                      
                # Affichage du dictionnaire
                print("fvgyhjkdfgvbjfdb",des_article)
                for article_code in codes : 
                        print(article_code)
                        article_id = extract_article_id( "https://pp-unum-back.etcinfo.tech/api/societe/articles",article_code, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
                        print("article_id",article_id)
                        ligne_article = extract_article_info("https://pp-unum-back.etcinfo.tech/api/societe/piece/article-details",article_id,token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
                        articles.append(ligne_article)
                        print("article",articles)
                if (nom_client and code_client) or code_client:
                   
                    # Use extracted client info to update facture_data
                    clients = extract_clients_info('https://pp-unum-back.etcinfo.tech/api/societe/clients' , code_client ,token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
                    
                    #print("clients",clients)
                    additions_to_ask = {}
                    if clients :
                            for client in clients:
                                for detected_type, detected_value in client.items():
                                    if detected_type in facture_data["tier"]:
                                        facture_data["tier"][detected_type] = detected_value
                                    if detected_type in facture_data["adresseFacturation"]:
                                        facture_data["adresseFacturation"][detected_type] = detected_value
                                    if detected_type in facture_data["adresseLivraison"]:
                                        facture_data["adresseLivraison"][detected_type] = detected_value
                                    
                                    if detected_type =='idTier' :
                                        id_contact = extract_contact_info(detected_value, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
                                        facture_data['tier']['contact'] = id_contact
                                
                                   
                            for detected_type, detected_value in detected_info.items():
                                if detected_type in config and detected_value not in config[detected_type][2]:
                                    additions_to_ask[detected_type] = detected_value
                            if len(articles)>=1:   
                                for article in articles : 
                                    if article :  
                                        if quantity != None :           
                                                for code,quantite in des_article.items():
                                                    if code.lower() == article['code'].lower():  
                                                        quantite = int(quantite)  # Convert quantity to int
                                                        article['quantity'] = quantite  # Update quantity in ligne_article   
                                                        facture_data["lignes"].append(article)
                                        else:
                                            facture_data["lignes"].append(article)
                                        
                                        

                            
                            pied = extract_total_amount( "https://pp-unum-back.etcinfo.tech/api/societe/piece/total-amount",payload,token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
                            print("pied",pied)
                            facture_data["pied"] = pied
                                    
                            if additions_to_ask:
                                response = {
                                    'response': f"Les informations suivantes n'existent pas : " + ', '.join([f"{k} : {v}" for k, v in additions_to_ask.items()]) + ". Voulez-vous les ajouter ? (oui/non)",
                                    'context': 'awaiting_confirmation',
                                    'pending_additions': additions_to_ask,
                                    'facture_data': {key: value for key, value in facture_data.items() if value is not None}
                                }
                                session['context'] = 'awaiting_confirmation'
                                session['pending_additions'] = additions_to_ask
                                return jsonify(response)
                            else:
                                response = {
                                    'response': "Toutes les informations détectées sont déjà présentes. taper confirmer",
                                    'context': 'initial',
                                    'facture_data': {key: value for key, value in facture_data.items() if value is not None}
                                }
                                session['context'] = 'initial'
                                return jsonify(response)
                    else:
                                response = {
                                    'response': "client n'existe pas",
                                    'context': 'initial',
                                    'facture_data': {key: value for key, value in facture_data.items() if value is not None}
                                }
                                session['context'] = 'initial'
                                return jsonify(response)
                                
                else:
                        
                        response = {
                            'response': "Pour ajouter une facture, veuillez fournir les informations suivantes : code de client",
                            'context': 'initial',
                            'user_data': {key: value for key, value in facture_data.items() if value is not None}
                        }
                        session['context'] = 'initial'
                        return jsonify(response)

        else:

            answer = chatbot_logic(user_input, qa_data, "fr")
            print(answer)
            response = {
                'response': answer,
                'context': 'initial',
                'user_data': {key: value for key, value in facture_data.items() if value is not None}
            }
            session['context'] = 'initial'
            return jsonify(response)

    elif context == 'awaiting_confirmation' or tag1 == "oui" or tag1 == "non":
        tag = closest_tag(user_input, qa_data, "fr")

        if tag == "oui":
            for item_type, item_value in pending_additions.items():
                id = ajouter_option(item_type, item_value)
                facture_data[item_type] = id 
            response = {
                'response': "Les informations suivantes ont été ajoutées avec succès : " + ', '.join([f"{k} : {v}" for k, v in pending_additions.items()]) + ". Voulez-vous ajouter autre chose ? si non taper confirmer",
                'context': 'initial',
                'facture_data': {key: value for key, value in facture_data.items() if value is not None},
                #'item_value': item_value,
                'pending': pending_additions
            }
            session['context'] = 'initial'
            session['pending_additions'] = {}
            return jsonify(response)
        elif tag == "non":
            for item_type, item_value in pending_additions.items():
                facture_data[item_type] = {
                    '@id': '/api/societe/forme-juridiques/10',
                    '@type': 'FormeJuridique',
                    'id': 10,
                    'codeInsee': None,
                    'libelle': None,
                    'typeForme': 2,  # Replace with appropriate legal form type if needed
                    'estPredefini': False,  # Modify as per your needs
                    'estDefault': False,  # Modify as per your needs
                    'estDesactive': False  # Modify as per your needs
                }
            response = {
                'response': "D'accord, l'ajout de nouvelles informations est annulé. taper confirmer ",
                'context': 'initial',
                'facture_data': {key: value for key, value in facture_data.items() if value is not None}
            }
            session['context'] = 'initial'
            session['pending_additions'] = {}
            return jsonify(response)
        else:
            response = {
                'response': "Je n'ai pas compris votre réponse. Voulez-vous ajouter les informations mentionnées ? Répondez par 'oui' ou 'non'.",
                'context': 'awaiting_confirmation',
                'pending_additions': pending_additions,
                'facture_data': {key: value for key, value in facture_data.items() if value is not None}
            }
            return jsonify(response)

    elif context == 'initial' and tag1 == "confirmer":
        check_etat = {}
        for ligne in facture_data['lignes']:
                article_id = ligne['articleId']  
                quantity = ligne['quantity'] 
                code_article = ligne['code']
                etat =check_stock(article_id, quantity, api_url="https://pp-unum-back.etcinfo.tech/api/societe/piece/article-quantites", token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
                check_etat[code_article] = etat
        code_etat = []
        for code_art , value in check_etat.items():
                    if value == False: 
                          code_etat.append(code_art)
                          break
        if len (code_etat) >=1 :
                        code_id = code_etat[0] 
                        response = {
                                    'response': f"Stock d'article de code {code_id} est introuvable",
                                    'context': 'initial'
                                }
                        articles.clear()
                        facture_data['lignes'].clear()
                        code_etat.clear()
                        session['context'] = 'initial'
                        return jsonify(response)                
                      
        else :

                        resultat = add_facture(facture_data, api_url="https://pp-unum-back.etcinfo.tech/api/societe/factures", static_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjEyOTAyMzIsImV4cCI6MTcyMTMyNjIzMiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdLCJzY2hlbWFBY3RpdmUiOiJnZXN0aW9uX3ByZXByb2RfMTRfMDYiLCJjb21wYW55IjpbeyJub20iOiJFVEMiLCJjb2RlIjoiQ09MSSIsImFjdGl2ZSI6ZmFsc2V9LHsibm9tIjoiU09MQVZJVEUiLCJjb2RlIjoiU09MQSIsImFjdGl2ZSI6dHJ1ZX1dLCJub20iOiJhbGljZSIsInVzZXJuYW1lIjoiYWxpY2V2MkBldGNpbmZvLmZyIiwic29jaWV0ZSI6MX0.pgyX1-NWwvmA1NJvMcWTScXNqKSG58cBv7hsrSatr_jO26Dl7UePZ-Jngh4j65Rtb4AB6SBvXIHQxJmYLkkAe-AdUVA9TQm1ikGdCfi_m42yf_ySCibYRUZarr2PzhozXugUg3iW9aVPcKxwo2QgW8DvjwmWvVe59HiubC8Pk79y59gn0X6YUiBTTUEOWBCiK9kexinISNWoqh-b5v8zXMadSR5MDcJF0dsK4ExGRYxMI5nMHNe-BJjuR9YeAE7Fl-rk7J4JPWMFGump-fijWVZzeCMp6sDxZM4OZvb8ggCI0l7nrvoS1kBeU8UByC6eBBUA7rubvViA03XfqWYoAw")
                        articles.clear()
                        facture_data['lignes'].clear()
                        if resultat:
                                    response = {
                                        'response': f"facture ajouté avec succès.",
                                        'context': 'initial',
                                        'facture_data': {key: value for key, value in facture_data.items() if value is not None}
                                    }
                                    session['context'] = 'initial'
                                    session['pending_additions'] = {}
                                    return jsonify(response)
                        else :
                                    response = {
                                        'response': f"Échec de l'ajout de la facture. Veuillez réessayer..",
                                        'context': 'initial',
                                        'facture_data': {key: value for key, value in facture_data.items() if value is not None}
                                    }
                                    session['context'] = 'initial'
                                    session['pending_additions'] = {}
                                    return jsonify(response)
                
    else:
        response = {
            'response': "Je n'ai pas compris votre demande. Pouvez-vous répéter ?",
            'context': 'initial'
        }
        session['context'] = 'initial'
        return jsonify(response)

if __name__ == '__main__': 
    app.run(debug=True ,host='0.0.0.0')

