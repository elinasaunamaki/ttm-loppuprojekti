import json
import boto3
'''
Function for publishing a message to MQTT topic at the press of an IoT button.
'''
def lambda_handler(event, context):
    client = boto3.client('iot-data', region_name='us-east-1')
    pay=json.dumps({"foo": "takeaphoto"})
    response = client.publish(
        topic='ttmTestiTopic/iot',
        qos=1,
        payload=pay
    )
    print(pay)
    
    return response