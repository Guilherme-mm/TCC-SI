"""
@author Guilherme Muller Moreira <guilherme.muller.m@gmail.com>
@version 0.1
@creation 05/05/2019

Description
-----------
    This file contains the declaration of a API designed to be used by the comand line tools
"""
import socket
import threading
import sys
from ApiMessage import ApiMessage

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('python-daemon', 10000)
sock.bind(server_address)

#Creating the shared message queue
waitingMessages = []
waitingResponses = []

def MessageProcessor():
    while True:
        if len(waitingMessages) > 0:
            message = waitingMessages[0]
            print ('received {} bytes from {}'.format(len(message.getMessageBody()), message.getSenderAddress()))
            
            response = ApiMessage(message.getMessageBody(), server_address[0], server_address[1], message.getSenderAddress(), message.getSenderPort())
            waitingResponses.append(response)
            waitingMessages.pop(0)

def ResponseDispatcher():
    while True:
        if len(waitingResponses) > 0:
            response = waitingResponses[0]
            sent = sock.sendto(response.getMessageBody(), (response.getReceiverAddress(), response.getReceiverPort()))
            print('sent {} bytes back to {} on {}'.format(sent, response.getReceiverAddress(), response.getReceiverPort()))
            waitingResponses.pop(0)

def MessageReceiver():
    while True:
        data, address = sock.recvfrom(4096)
        
        message = ApiMessage(data, address[0], address[1], server_address[0], server_address[1])
        waitingMessages.append(message)

if __name__ == "__main__":
    threading.Thread(target = MessageReceiver).start()
    threading.Thread(target = MessageProcessor).start()
    threading.Thread(target = ResponseDispatcher).start()