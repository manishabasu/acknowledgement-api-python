import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'AcknowledgementTableNew'  # Replace with your DynamoDB table name

def post_ack(event, context):
    body = json.loads(event['body'])

    request_id = body.get('request_id')
    acknowledgment = body.get('acknowledgment')

    if not request_id or acknowledgment is None:
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing request_id or acknowledgment in the request body'}),
        }
    else:
        try:
            table = dynamodb.Table(table_name)
            print('request_id:'+request_id)
            table.update_item(
                Key={'request_id': request_id},
                UpdateExpression='SET acknowledgment = :acknowledgment',
                ExpressionAttributeValues={':acknowledgment': acknowledgment}
            )
            response = {
                'statusCode': 200,
                'body': json.dumps({'message': 'Acknowledgment stored successfully'}),
            }
        except Exception as e:
            response = {
                'statusCode': 500,
                'body': json.dumps({'error': 'An error occurred while processing the request'}),
            }

    return response
