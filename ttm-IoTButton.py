import json
import boto3
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def lambda_handler(event, context):
    client = boto3.client('iot-data', region_name='us-east-1')
    pay=json.dumps({"foo":"bar"})
    response = client.publish(
        topic='ttmTestiTopic/iot',
        qos=1,
        payload=pay
    )
    print(pay)
    
    return response