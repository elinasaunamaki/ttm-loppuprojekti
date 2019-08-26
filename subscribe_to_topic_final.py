from picamera import PiCamera
import boto3
import time
import os
import logging
from botocore.exceptions import ClientError
from signal import pause
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from ttmcapturephoto import *
import json
import pygame
from ttmpolly import Polly

'''
Script to subscribe Raspberry Pi to topic linked with IoT-Button and handle different messages accordingly.
'''

def customCallback(client, userdata, message):

    if json.loads(message.payload)=={'foo': 'epicfail'}:
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("No Faces detected!")
        print("--------------\n\n")
        tts = Polly('Amy')
        tts.say('<speak>No faces detected. Please try again.</speak>')

    elif json.loads(message.payload)=={'foo': 'takeaphoto'}:
        print("Received a new message: ")
        capturephoto()
    else:
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("Siirrytaan Pollyyn!")
        message=json.loads(message.payload)
        tts = Polly('Matthew')
        prosentti="percent"
        list=[] #create a list for different emotions and append right values and words correctly for Polly to synthesize
        for key in message:
            list.append(message[key]),
            list.append(prosentti),
            list.append(key),
            list.append('<break time="0.2s"/>')
        print(list)
        sentence = ' '.join(list)
        sentence = '<speak>Thank you. Your current emotions seem to be: {} .</speak>'.format(sentence)
        tts.say(sentence)
        print(sentence)
        return True


host = #HOST
port = #PORT
rootCAPath = #CA PATH
certificatePath = #CERTIFICATE PATH
privateKeyPath = #KEY PATH
clientId = #CLIENT ID
topic = #TOPIC
payload= #PAYLOAD NAME

logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId) #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
#AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
pause()
