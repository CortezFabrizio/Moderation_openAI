import requests
import openai
from flask import Flask,request
import json
import os

app = Flask(__name__)

key = os.getenv('openai_key')

endpoint = 'https://api.openai.com/v1/moderations'

header = {'Content-Type':'application/json','Authorization':f'Bearer {key}'}

openai.api_key = key


@app.route("/", methods=['POST'])
def search():

    text_entered = request.json['text']

    input_text = {'input':text_entered}

    openai_res = requests.post(url=endpoint,headers=header,json=input_text).content
    openai_results = json.loads(openai_res)["results"][0]


    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.1,
        max_tokens=1,
        messages=[
                {"role": "user", "content":f"If this text mentions an illegal drug and the context proves it,say True : '{text_entered}' "}
                
            ]
        )

    is_drug_content = chat_completion['choices'][0]['message']['content'].upper()

    is_flagged = openai_results['flagged']

    categories = openai_results['categories']

    if is_drug_content == 'TRUE':
        categories['drugs'] = True
        if not is_flagged:
            is_flagged = True
    else:
        categories['drugs'] = False


    return {'flagged':is_flagged,'categories':categories}


