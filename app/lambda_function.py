from app import app
import awsgi
import json

def lambda_handler(event, context):
    # Convertir los objetos event y context a JSON
    event_json = json.dumps(event)
    context_json = json.dumps({
        "function_name": context.function_name,
        "function_version": context.function_version,
        "invoked_function_arn": context.invoked_function_arn,
        "memory_limit_in_mb": context.memory_limit_in_mb,
        "aws_request_id": context.aws_request_id,
        "log_group_name": context.log_group_name,
        "log_stream_name": context.log_stream_name,
    }, default=str)  # default=str para manejar objetos que no son serializables por defecto

    # Imprimir los objetos JSON
    print("event")
    print(event_json)
    print("context")
    print(context_json)

    # Verificar la presencia de 'httpMethod' en el evento
    if 'httpMethod' not in event:
        error_message = "Missing key: 'httpMethod'"
        print(error_message)  # Para registro en los logs de CloudWatch
        return {
            'statusCode': 400,
            'body': json.dumps({
                'errorMessage': error_message,
                'event': event
            })
        }

    # Manejar el evento con awsgi
    ###try:
        return awsgi.response(app, event, context)
    #except Exception as e:
        # Manejar cualquier excepción no anticipada y devolver un error 500
      #  error_message = f"Internal server error: {str(e)}"
       # print(error_message)  # Para registro en los logs de CloudWatch
        #return {
          #  'statusCode': 500,
           # 'body': json.dumps({
           #     'errorMessage': error_message,
            #    'event': event
           # })
       # }

