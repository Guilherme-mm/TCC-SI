import threading
import json
from flask import Flask, request, Response
from ..control.GERTController import GERTController
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/routines/<routineName>/<operation>', methods=['GET'])
def routines(routineName, operation):
    return '{} routine will {}'.format(routineName, operation)

@app.route('/routines/update-model', methods=['GET'])
def startModelUpdate():
    controller = GERTController()
    controller.clearGraphDB()
    controller.clearDataDB()
    controller.updateModel()
    return "success"

@app.route('/get-recommendations', methods=['POST'])
def getRecommendations():
    parameters = request.json
    controller = GERTController()
    recommendations = controller.getRecommendations(parameters["actor"], int(parameters["quantity"]))
    recommendations = json.dumps(recommendations)
    return Response(recommendations, mimetype='application/json')

@app.route('/similarity-engine', methods=['POST'])
def setSimilarityEngine():
    parameters = request.json
    controller = GERTController()
    controller.setSimilarityEngine(parameters["engine"])
    return "success"

# if __name__ == '__main__':
def run():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

threading.Thread(target=run).start()
