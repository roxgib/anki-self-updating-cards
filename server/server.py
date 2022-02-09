from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

from data.wolfram import getAnswer

app = Flask('Self-Updating Cards')
api = Api(app)

@app.route('/')
def hello_world():
    return 'Self-Updating Cards'

@app.route('/query', methods=['GET'])
def query():
    question = request.args.get('question')
    if 'format' in request.args:
        format = request.args['format']
    else:
        format = None

    if 'location' in request.args:
        location = request.args['location']
    else:
        location = None

    if 'appid' in request.args:
        appid = request.args['appid']
    else:
        appid = None
    
    answer = getAnswer(question)

    return {'answer': answer}, 200

if __name__ == '__main__':
    app.run()