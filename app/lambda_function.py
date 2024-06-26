from app import app
import awsgi
import json
#import sys

def lambda_handler(event, context):      
    #search_path = sys.path
    #print(search_path)
    # Convertir los objetos event y context a JSON
    event_json = json.dumps(event, indent=4)
    context_json = json.dumps(context, indent=4, default=str)  # default=str para manejar objetos que no son serializables por defecto

    # Imprimir los objetos JSON
    print("event")
    print(event_json)
    print("context")
    print(context_json)
    
    return awsgi.response(app, event, context)
