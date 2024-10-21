import json
import os
import string
import random
import boto3
from boto3.dynamodb.conditions import Key

table_name = os.environ['TABLE_NAME']

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

# Generate a random short URL
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Lambda handler function
def handler(event, context):
    if event['httpMethod'] == 'POST':
        # Shorten the URL
        body = json.loads(event['body'])
        long_url = body.get('longUrl')

        # Generate short URL
        short_url = generate_short_url()

        # Store in DynamoDB
        table.put_item(
            Item={
                'shortUrl': short_url,
                'longUrl': long_url
            }
        )

        # Return the short URL
        return {
            'statusCode': 200,
            'body': json.dumps({'shortUrl': short_url})
        }

    elif event['httpMethod'] == 'GET':
        # Redirect to the long URL
        short_url = event['pathParameters']['shortUrl']

        # Query DynamoDB for the long URL
        response = table.get_item(
            Key={
                'shortUrl': short_url
            }
        )

        item = response.get('Item')
        if item:
            long_url = item['longUrl']
            return {
                'statusCode': 301,
                'headers': {
                    'Location': long_url
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'URL not found'})
            }

    return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Unsupported method'})
    }