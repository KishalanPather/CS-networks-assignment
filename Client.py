from socket import *
import threading
import os

serverName = "192.168.56.1"
serverPort = 12000
name = "aj"        # our own name
ourIP = "192.168.56.1"
ourPort = 15000     # must be unique if you are running multiple cients on the same machine
ipAndPortOfSomeContact = []     # when the server send the ip and port of a person we are trying to message it gets stored here
allContactsMessaged = []  # there names ip and port all stored in this order

privacyStatus = input("Would you like to be private or public on the server?\n")
privacyStatus = privacyStatus.lower()

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))      # just making tcp connection to server

serverResponse = clientSocket.recv(1024).decode()       # server will start the communication by 
if(serverResponse == "NAME&PORT&PRIVACYSTATUS"):
    clientSocket.send((name + "," + str(ourPort) + "," + privacyStatus).encode())                # send the server our name so it can store it in its list of clients

def receiveIncomingMessagesFromServer(clientSocket):
    try:
        while True:
            incomingMessage = clientSocket.recv(1024).decode()
            if(incomingMessage[:6] == "123123"):
                print(incomingMessage[6:])
            else:   
                ipAndPortOfSomeContact.append(incomingMessage)
    except ConnectionAbortedError:
        pass
 
def messageContact(ipAddress, port, message):
    privateUDPSocket = socket(AF_INET, SOCK_DGRAM)
    privateUDPSocket.sendto((name + ": " + message).encode(), (ipAddress, int(port)))
    privateUDPSocket.close()

# we also need a thread which is constantly running and accepting connection requests from other clients when they private message us
def acceptConnectionRequests():
    acceptConnectionSocket = socket(AF_INET, SOCK_DGRAM)
    acceptConnectionSocket.bind((ourIP, ourPort))
    while True:
        message, addr = acceptConnectionSocket.recvfrom(1024)
        print(message.decode())  # this would be incoming messages from other contacts     
        
thready = threading.Thread(target= receiveIncomingMessagesFromServer, args = (clientSocket,))        
thready.start()
threadx = threading.Thread(target=acceptConnectionRequests, )
threadx.start()
response = input("Would you like to send a Group Message(G) or a Private Message(P) or a List of all Clients available(L)?\n")
try:
    while(response != "EXIT"):
        if(response == "G"):
            response = input("What would you like to send?\n")
            clientSocket.send(("G," + name + ": " + response).encode())
        elif(response == "P"):
            recipient = input("Who would you like to send a private message to?\n")
            response = input("What would you like to send?\n")
            found = False
            for items in allContactsMessaged:
                if(items[0] == recipient):
                    ipAndPortOfSomeContact.append(items[1] + "," + items[2])
                    found = True
                    break
            if(found == False):
                clientSocket.send(("P," + recipient + "," + response).encode())
            # server must respond by sending us the IP address and the port of the contact we are trying to message and then we make a connection to them

            while(len(ipAndPortOfSomeContact) < 1):
                # basically wait till the message arrives from server and is put in the list of contacts list
                pass       
            incomingMessage = ipAndPortOfSomeContact[0]
            ipAndPortOfSomeContact.clear()
            if(incomingMessage != "Error"):
                parts = incomingMessage.split(",")
                theIP =  parts[0]
                thePort =  parts[1]
                allContactsMessaged.append([recipient, theIP, thePort])

            # now create a new thread to send a private message to this contact we are trying to message
                thread = threading.Thread(target = messageContact, args = (theIP, thePort,  response,))
                thread.start()
                thread.join()
            else:
                print("The client does not exist or is set to private.\n")
        elif(response == "L"):
            clientSocket.send(("L, ").encode())
            while(len(ipAndPortOfSomeContact) < 1):
                # basically wait till the message arrives from server and is put in the list of contacts list
                pass  
            incomingList = ipAndPortOfSomeContact[0]
            ipAndPortOfSomeContact.clear()
            print("The following clients are available: ")
            print(incomingList)
        response = input("Would you like to send a Group Message(G) or a Private Message(P) or a List of all Clients available(L)?\n")
    clientSocket.close()
    os._exit(0)
except ConnectionAbortedError:
    pass


