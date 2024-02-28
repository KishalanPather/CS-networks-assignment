from socket import *
import threading

serverName = "192.168.0.125"
serverPort = 12000
name = "john"        # our own name
ourPort = 13000
listOfContacts = []


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

serverResponse = clientSocket.recv(1024).decode()
if(serverResponse == "NAME&PORT"):
    clientSocket.send((name + "," + str(ourPort)).encode())                # send the server our name so it can store it in its list of clients


def receiveIncomingMessagesFromServer(clientSocket):
    while True:
        print("the code is entering this section")
        incomingMessage = clientSocket.recv(1024).decode()
        print("this piece of code is running!!!")
        if(incomingMessage == ""):
            continue
        if(incomingMessage[:6] == "123123"):
            listOfContacts.append(incomingMessage[7:])
        else:
            print(incomingMessage)
        incomingMessage = ""
            

 
def messageContact(ipAddress, port, message):
    privateSocket = socket(AF_INET, SOCK_STREAM)
    privateSocket.connect((ipAddress, port))
    privateSocket.send((name + ": " + message).encode())
    privateSocket.close()

# we also need a thread which is constantly running and accepting connection requests from other clients when they private message us
def acceptConnectionRequests():
    acceptConnectionSocket = socket(AF_INET, SOCK_STREAM)
    acceptConnectionSocket.bind(("192.168.0.125", ourPort))
    acceptConnectionSocket.listen(3)
    while True:
        client, addr = acceptConnectionSocket.accept()
        print(client.recv(1024).decode())  # this would be incoming messages from other contacts     
        
thready = threading.Thread(target = receiveIncomingMessagesFromServer, args=(clientSocket,))
thready.start()
threadx = threading.Thread(target=acceptConnectionRequests, )
threadx.start()
response = input("Would you like to send a Group Message(G) or a Private Message(P)?\n")
while(response != "EXIT"):
    if(response == "G"):
        response = input("What would you like to send?\n")
        clientSocket.send(("G," + response).encode())
    elif(response == "P"):
        recipient = input("Who would you like to send a private message to?\n")
        response = input("What would you like to send?\n")
        clientSocket.send((recipient + "," + response).encode())
        # server must respond by sending us the IP address and the port of the contact we are trying to message and then we make a connection to them
        #theIPAndPort = listOfContacts[0]
        #parts = theIPAndPort.split(",")
        theIP =  "192.168.0.125"  # parts[0].split("(")[1].strip("'")
        thePort =  14000  # parts[2]
        #listOfContacts.clear()
        # now create a new thread to send a private message to this contact we are trying to message
        thread = threading.Thread(target = messageContact, args = (theIP, thePort, response,))
        thread.start()
        thread.join()
    response = input("Would you like to send a Group Message(G) or a Private Message(P)?\n")
        
    
clientSocket.close()
