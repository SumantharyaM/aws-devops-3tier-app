import boto3

def get_items():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('YourDynamoTableName')
    response = table.scan()
    return response['Items']

