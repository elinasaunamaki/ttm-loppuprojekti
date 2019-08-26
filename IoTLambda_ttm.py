import json
import boto3
'''
Function for publishing a message to MQTT topic at the press of an IoT button.
'''
def lambda_handler(event, context):
    client = boto3.client('iot-data', region_name='<REGION>')
    pay=json.dumps({"foo": "takeaphoto"})
    response = client.publish(
        topic='<TOPIC>',
        qos=1,
        payload=pay
    )
    print(pay)
    
    return response