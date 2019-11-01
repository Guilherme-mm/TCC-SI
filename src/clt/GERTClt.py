import socket
import threading
import json
import click

from ApiMessage import ApiMessage
from MessageType import MessageType

service_address = ('python-daemon', 10000)
clt_address = ('python-clt', 10000)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(clt_address)


def SendMessage(message):
    # print('Sending: [{}]...'.format(message.getMessageBody()))
    # print("")
    sock.sendto(message.getMessageBody().encode('utf-8'), (message.getReceiverAddress(), message.getReceiverPort()))

def MessageReceiver():
    while True:
        data, server = sock.recvfrom(4096)
        data = data.decode('utf-8')
        messageBody = json.loads(data)
        if messageBody["messageType"] == MessageType.END.value:
            try:
                print('{}'.format(messageBody["messageContent"]))
            except KeyError:
                print(messageBody)

            exit()
        if messageBody["messageType"] == MessageType.CONTINUATION.value:
            print('{}'.format(messageBody["messageContent"]))

@click.group()
def cli():
    pass

@cli.command()
@click.option('--body', default = 'test message', help = 'Content of the message to be sent')
def sendMessageToService(body):
    message = ApiMessage(body, clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
@click.option('--path', help='Location of the log files from where data will be collected')
def setLogPath(path):
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 1 #Set log path
    messageBody["messageContent"]["path"] = path
    messageBody["messageType"] = 1 #Begin
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
def updateModel():
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 2 #update model
    messageBody["messageType"] = 1 #Begin
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
@click.option('--engine', default = 'simpleEuclidian', help='The name of the similarity engine to be used')
def setSimilarityEngine(engine):
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 3 #Set similarity engine
    messageBody["messageContent"]["similarityEngineName"] = engine
    messageBody["messageType"] = 1 #Begin
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
@click.option('--algorithm', default="hierarchicalCluster", help="The name of the clustering algorithm")
def setClusterAlgorithm(algorithm):
    messageBody = {}
    messageBody["operationCode"] = 4
    messageBody["messageType"] = 1 #Begin
    messageBody["clusterAlgorithmName"] = algorithm
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
@click.option('--algorithm', default="KNN", help="The name of the recomendation selection algorithm")
def setRecommendationSelectionAlgorithm(algorithm):
    messageBody = {}
    messageBody["operationCode"] = 5
    messageBody["messageType"] = 1 #Begin
    messageBody["recommendationSelectionAlgorithmName"] = algorithm
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
@click.option('--actor', help="The identifier of the actor that will receive recommendations")
@click.option('--quantity', default=10, help="The number of recommendations desired")
def getRecommendations(actor, quantity):
    messageBody = {}
    messageBody["operationCode"] = 6
    messageBody["messageType"] = 1 #Begin
    messageBody["actorId"] = actor
    messageBody["quantity"] = quantity
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)


@cli.command()
@click.option('--path', help="The path to the file containing the test data samples")
def setTestDataPath(path):
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 7 #Set test data path
    messageBody["messageContent"]["path"] = path
    messageBody["messageType"] = 1 #Begin
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
def testRecommendationsAccuracy():
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 8 #Test Accuracy
    messageBody["messageType"] = 1 #Begin
    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
def clearGraphDB():
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 9 #Clear DB
    messageBody["messageType"] = 1 #Begin

    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
def clearDataDB():
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 10 #Clear DB
    messageBody["messageType"] = 1 #Begin

    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

@cli.command()
@click.option('--name', help="The configuration name")
def getConfigurationValue(name):
    messageBody = {}
    messageBody["messageContent"] = {}
    messageBody["messageContent"]["operationCode"] = 11 #Get config
    messageBody["messageContent"]["configurationName"] = name
    messageBody["messageType"] = 1 #Begin

    message = ApiMessage(json.dumps(messageBody), clt_address[0], clt_address[1], service_address[0], service_address[1])
    SendMessage(message)

if __name__ == "__main__":
    threading.Thread(target = MessageReceiver).start()
    cli()
