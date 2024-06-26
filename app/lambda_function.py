from app import app
import awsgi
import json

def lambda_handler(event, context):
    # Convertir los objetos event y context a JSON
    event_json = json.dumps(event)
 
    # Imprimir los objetos JSON
    print("event")
    print(event_json)
   

   
    return awsgi.response(app, event, context)
   
