import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . import helper
import os
import boto3

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        self.s3 = boto3.client('s3', region_name='us-east-1', 
                  aws_access_key_id=os.environ['AWS_KEY'], 
                  aws_secret_access_key=os.environ['AWS_SECRET'])
        
        self.bucket_name = 'data2dialog'
        self.files = {}
        
    def receive(self, text_data):
        try:
            # Convert the received text data from JSON format to Python dictionary
            text_data_json = json.loads(text_data)

            # Extract the message from the received data
            question = text_data_json['message']
            file_key = text_data_json['file_key']
            
            # if chat is being executed for the first time
            if file_key not in self.files:
                # get data from s3
                self.files[file_key] = helper.read_csv_from_s3(self.s3, self.bucket_name, file_key)
                print('Got file')
            
            # ask openai about it
            result = helper.ask_openai_to_code(question,self.files[file_key])
            
            # Send the acknowledgment back to the client
            self.send(json.dumps({'message': result}))
        
        except:
            self.send(json.dumps({'message': "I ran into an error, I'm sorry but I am still under development!"}))
            
    