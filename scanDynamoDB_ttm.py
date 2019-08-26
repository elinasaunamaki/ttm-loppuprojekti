import boto3
import json
import time
import uuid
import logging
from decimal import Decimal
from botocore.exceptions import ClientError
'''
Function to scan DynamoDB table and upload the data to an S3 bucket.
'''
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('ttm')
def lambda_handler(event, context):
    
    #Helper function to convert decimals in the response to floats.
    def handle_decimal_type(obj):
        if isinstance(obj, Decimal):
            if float(obj).is_integer():
                return int(obj)
            else:
                return float(obj)
        raise TypeError
    
    response = table.scan()
    body = json.dumps(response['Items'], default=handle_decimal_type)
    response = s3.put_object(Bucket='ttm-quicksightfiles',
    Key = 'quicksightfile.json', Body=body, ContentType='application/json')