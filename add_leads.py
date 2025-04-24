import json
from notion_client import Client
from dotenv import load_dotenv
import os


load_dotenv()

LEADS_NOTION_KEY = os.getenv('LEADS_NOTION_KEY')
LEADS_DATABASE_ID = os.getenv('LEADS_DATABASE_ID')

def send_response(status:int, body:str):
    return {
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'statusCode': status,
        'body': body
    }

def add_new_lead(event, context):
    body = json.loads(event['body'])

    name = body.get('name')
    email = body.get('email')
    product = body.get('product')
    message = body.get('message')
    lead_source = body.get('lead_source')
    honey_pot = body.get('honey_pot')

    if honey_pot != "":
        return send_response(400, f"Spam Detected")

    if not name or not email or not product or not message or not lead_source:
        return send_response(422, f"Incompleted data")
    

    try:
        notion = Client(auth=LEADS_NOTION_KEY)
        database_id = LEADS_DATABASE_ID

        new_page = {
            "parent": { "database_id": database_id },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": name
                            }
                        }
                    ]
                },
                "Email": {
                    "email": email
                },
                "Product": {
                    "select": {
                        "name": product
                    }
                },
                "Message": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": message
                            }
                        }
                    ]
                },
                "Lead Source": {
                    "select": {
                        "name": lead_source
                    }
                }
            }
        }
        notion.pages.create(**new_page)

        return send_response(200, "Created with sucess")
    except Exception as e:
        print(e)
        return send_response(500, f"Error adding lead - {e}")
    

# if __name__ == "__main__":
    # req = {
    #     "resource": "/update",
    #     "path": "/update",
    #     "httpMethod": "POST",
    #     "headers": {
    #         "Content-Type": "application/json"
    #     },
    #     "queryStringParameters": {},
    #     "body": "{ \"name\": \"Leonardo Leite\", \"email\": \"Leonardo@email.com\", \"product\": \"both\", \"message\": \"Ola, quero usar a MARiA\", \"lead_source\": \"Site\" }",
    #     "isBase64Encoded": False
    # }
#     print(add_new_lead(req, {"is_local": True}))