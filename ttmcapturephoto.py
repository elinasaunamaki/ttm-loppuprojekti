from picamera import PiCamera
import boto3
import time
import os
import logging
from botocore.exceptions import ClientError
#from ttmpolly import Polly
def capturephoto():
    camera = PiCamera()
    image_path = '/home/pi/ttm/image_%s.jpg' % int(round(time.time() * 1000))
    camera.capture(image_path)
    print('Took photo')
    image = image_path[13:]
    camera.close()

    def upload_to_aws(local_file, bucket, s3_file=None):
       if s3_file is None:
           s3_file = local_file
       s3 = boto3.client('s3')

       try:
           s3.upload_file(local_file, bucket, s3_file)
           os.remove(local_file)
       except ClientError as e:
           logging.error(e)
           return False


       return True
    upload_to_aws(image, 'ttm-photos')
    #tts = Polly('Amy')
    #time.sleep(10)
    #tts.say('Analyzing photo. Please wait.')