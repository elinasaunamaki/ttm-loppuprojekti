import json
import boto3
import uuid
import time
'''
Script that is invoked when a photo is uploaded to an S3 bucket
for analyzing the photo with Rekognition, uploading the data to DynamoDB
and publishing a message to MQTT topic. 
'''
def lambda_handler(event, context):
    #Getting the bucket and file names from the event for Rekognition to use. 
    bucket = event['Records'][0]['s3']['bucket']['name']
    fileName = event['Records'][0]['s3']['object']['key']
    
    client=boto3.client('rekognition')
    
    feelingsdict = {}
    pollydict = {}
    uniqueid = uuid.uuid4()
    aika = int(round(time.time() * 1000))
    
    #Sending the photo to Rekognition
    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},Attributes=['ALL'])
    #Going through the response from Rekognition and creating feelingsdict for DynamoDB and pollydict for user feedback.
    if response['FaceDetails'] != []:
        for label in response['FaceDetails'][0]["Emotions"]:
            feelingsdict[label['Type']] = str(label['Confidence'])
            smile = response['FaceDetails'][0]['Smile']['Value'] #getting smile boolean
    
        for item in response['FaceDetails'][0]["Emotions"]:
            if (item['Confidence']) >= 2:
                pollydict[item['Type'].lower()] = str(round(item['Confidence']))       
        #Publishing user feedback to MQTT topic.
        client = boto3.client('iot-data', region_name='us-east-1')
        pay=json.dumps(pollydict)
        resp = client.publish(
            topic='ttmTestiTopic/iot',
            qos=1,
            payload=pay
        )
        
    else:
        print('No face detected.')
        client = boto3.client('iot-data', region_name='us-east-1')
        pay=json.dumps({"foo": "epicfail"})
        resp = client.publish(
            topic='ttmTestiTopic/iot',
            qos=1,
            payload=pay
        )
    
    #Uploading the data to DynamoDB.
    if response['FaceDetails'] != []:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('ttm')
        response = table.put_item(
            Item={
                'id': str(uniqueid),
                'aikaleima': aika, #timestamp in milliseconds
                'smile': smile,
                'happy': feelingsdict['HAPPY'],
                'fear': feelingsdict['FEAR'],
                'calm': feelingsdict['CALM'],
                'sad': feelingsdict['SAD'],
                'surprised': feelingsdict['SURPRISED'],
                'angry': feelingsdict['ANGRY'],
                'confused': feelingsdict['CONFUSED'],
                'disgusted': feelingsdict['DISGUSTED']
            }
        )
        print('PutItem succeeded')
    #Deleting the photo from the S3 bucket after everything has been done.    
    client = boto3.client('s3')
    response666 = client.delete_object(
    Bucket=bucket,
    Key=fileName
    )
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
