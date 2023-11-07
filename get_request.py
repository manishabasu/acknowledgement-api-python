import json
import boto3
import logging


dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table_name = "AcknowledgementTableNew"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_request(event,context):
    request_id = event['pathParameters']['request_id']
    print('request_id:'+request_id)


    if not request_id:
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing request id in path parameters'})
        }
    else:
        try:
            data = client.get_item(
                TableName='AcknowledgementTableNew',
                Key={
                    'request_id': {
                        'S': request_id
                    }
                }
            )
            if 'Item' not in data:
                response = {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'data not present'})
            }
            else:
                response = {
                    'statusCode': 200,
                   'body' : json.dumps({'message': 'Success'}),
                }
        except Exception as e:
            response = {
                'statusCode' : 500,
                'body': json.dumps({'error': str(e)})
            }

    return response