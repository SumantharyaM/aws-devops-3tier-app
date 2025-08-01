import boto3
from botocore.exceptions import ClientError

def get_items():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('MyAppTable')
        response = table.scan()
        return response['Items']
    except ClientError as e:
        print("DynamoDB ClientError:", e)
        return {"error": str(e)}
    except Exception as e:
        print("General Exception:", e)
        return {"error": str(e)}
