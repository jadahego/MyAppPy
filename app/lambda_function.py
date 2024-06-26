from app import app
import awsgi
#import sys

def lambda_handler(event, context):      
    #search_path = sys.path
    #print(search_path)
    print("event")
    print(event)
    print("context")
    print(context)
    return awsgi.response(app, event, context)
