"""
@author Guilherme Muller Moreira <guilherme.muller.m@gmail.com>
@version 0.1
@creation 05/05/2019

Description
-----------
    This file contains the declaration of a API designed to be used by the comand line tools
"""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/routines/<routineName>/<operation>', methods=['GET'])
def startDataCollection(routineName, operation):
    return '{} routine will {}'.format(routineName, operation)

if __name__ == '__main__':
    app.run(host='0.0.0.0')