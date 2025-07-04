from django.shortcuts import render
from sqlalchemy import create_engine
from django.conf import settings
from django.http import JsonResponse
import os
import boto3
import uuid
import pandas as pd
from io import StringIO
from . import helper
import time

#Get S3 Bucket Credentials
s3 = boto3.client('s3', region_name='us-east-1', 
                  aws_access_key_id=os.environ['AWS_KEY'], 
                  aws_secret_access_key=os.environ['AWS_SECRET'])


def landing_page(request):
    return render(request, 'landing.html')


def main_page(request):
    return render(request, "main.html")

def upload_file_view(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']

        # Define S3 bucket name and file key (path)
        # file_key will always be unique
        bucket_name = 'data2dialog'
        filename = file.name.replace(" ", "_")
        file_key = f'{str(uuid.uuid4())}_{filename}'
        
        # Upload the file to S3
        s3.upload_fileobj(file, bucket_name, file_key)
        time.sleep(10)

        # Read the file's content directly from S3
        data = helper.read_csv_from_s3(s3, bucket_name,file_key)

        # Check if session already has any document
        if 'documents' not in request.session:
            request.session['documents'] = {}

        # Append document name to the user session
        request.session['documents'][file_key] = {'filename': filename, 'schema': data.dtypes.to_string()}

        return JsonResponse({'status': 'success', 'message': 'File uploaded successfully!', 'filename': file.name})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
    



def get_database_details(db_url):
    '''
    Function to get and store details about a schema of a database
    
    db_url: string      Constructor string for sqlAlchemy
    '''
    details = ''
    
    # Create a SQLAlchemy engine
    engine = create_engine(db_url)
    
    # Create a connection to the engine
    cursor = engine.connect()
    
    # Retrieve table names
    tables = cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    """)

    tables = [table[0] for table in tables]
    
    for table in tables:
        columns = cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s;
        """, (table,))

        col_str_list = [f"{col[0]} {col[1]}" for col in columns]
        col_str = ', '.join(col_str_list)

        details+=f"{table} ({col_str})\n"

    cursor.close()
    return details