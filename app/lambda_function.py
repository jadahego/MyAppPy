from app import app
import awsgi
import json
#import sys

def lambda_handler(event, context):      
    #search_path = sys.path
    #print(search_path)
    # Convertir los objetos event y context a JSON
    event_json = json.dumps(event)
    
    context_json = json.dumps(  {
        "function_name": context.function_name,
        "function_version": context.function_version,
        "invoked_function_arn": context.invoked_function_arn,
        "memory_limit_in_mb": context.memory_limit_in_mb,
        "aws_request_id": context.aws_request_id,
        "log_group_name": context.log_group_name,
        "log_stream_name": context.log_stream_name,
        # Puedes agregar más atributos si es necesario
    }, default=str)  # default=str para manejar objetos que no son serializables por defecto

    # Imprimir los objetos JSON
    print("event")
    print(event_json)
    print("context")
    print(context_json)

    return awsgi.response(app, event, context)
