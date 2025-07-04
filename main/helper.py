import boto3
import pandas as pd
from io import StringIO
import openai
import os


def read_csv_from_s3(s3, bucket_name, file_key):
    # Get the CSV file from S3 using the provided client instance
    print(s3, bucket_name, file_key)
    csv_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    csv_string = csv_obj['Body'].read().decode('utf-8')
    
    # Convert the CSV string to DataFrame
    df = pd.read_csv(StringIO(csv_string))
    
    return df



def execute_code(code, data):
    '''
    
    
    Inputs:
    code: string          python code written by ChatGPT
    data: dataframe       Pandas dataframe of the data uploaded by the user
    
    
    Outputs:

    '''
    
    local_vars = {"data": data}
    exec(code, globals(), local_vars)
    
    return local_vars.get('result', None)



def ask_openai_to_code(question, data):
    '''
    Function to ask a question from chatGPT 
    
    Inputs:
    question: string      Query made by the user in simple english words
    data: dataframe       Pandas dataframe of the data uploaded by the user
    
    
    
    Outputs:

    '''
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    prompt = f"""Based on the following description of a dataframe: data = 
    
        {data.dtypes.to_string()}
    
    Write Python code to get the answer to the following question:
        {question}
        
    Output only the Python code. Do not output anything else. Return final output in variable 'result'.
    
    Code = 
    """
    
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    
    response = response.choices[0]['message']['content']
    
    result = execute_code(response,data)
    
    prompt = f'''Based on the code written by you to answer the question:

        {question}
        
        We got the following results:
        
        {result}

        Insightfully Interpret these results in less than 30-100 words. Have conversational and analytical tone. Separate important results from other text wherever necessary.
    '''
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0]['message']['content']