import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
table_name = 'AcknowledgementTableNew'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)


def post_ack(event, context):
    request_data = json.loads(event['body'])
    data = request_data.get('data', {})
    print('Printing data:' + json.dumps(data))
    try:
        request_id = data.get('request_id')
        acknowledged = data.get('acknowledged', False)

        if not request_id or acknowledged is None:
            response = {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing request_id or acknowledged flag in the request body'}),
            }
        else:
            response = table.put_item(
                Item={'request_id': request_id,
                      'acknowledged': acknowledged
                      })
        # Prepare the response
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            body = {
                "message": "Item added successfully",
                "input": data
            }
            status_code = 200
        else:
            body = {
                "message": "Error adding item to DynamoDB",
                "error": response
            }
            status_code = 500
    except Exception as e:
        body = {
            "message": "Exception occured",
            "error": str(e)
        }
        status_code = 500

    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }
