import json
import awsgi

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

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

    try:
        return awsgi.response(app, event, context)
    except Exception as e:
        error_message = f"Internal server error: {str(e)}"
        print(error_message)  # Para registro en los logs de CloudWatch
        return {
            'statusCode': 500,
            'body': json.dumps({
                'errorMessage': error_message,
                'event': event
            })
        }


