from app import app
import awsgi
#import sys

def lambda_handler(event, context):      
    #search_path = sys.path
    #print(search_path)
    return awsgi.handle_request(app, event, context)
