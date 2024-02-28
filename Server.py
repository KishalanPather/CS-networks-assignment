from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("192.168.0.125", serverPort))
serverSocket.listen(3)
print("The server is running...")

clientNames = []
clientIP = []
clientPorts = []
clients = []



def connectToClients():
    while True:
        client, addr = serverSocket.accept()
        print("Connected to", addr)
        client.send("NAME&PORT".encode())
        clientNameAndPort = client.recv(1024).decode()
        clientName = clientNameAndPort.split(",")[0]
        clientPort = clientNameAndPort.split(",")[1]
        clientIP.append(addr)
        clientNames.append(clientName)
        clients.append(client)
        clientPorts.append(clientPort)
        print("Connection successful.")
        
        thread = threading.Thread(target=temp, args =(client,))
        thread.start()


        

    
def temp(client):
    clientsMessage = client.recv(1024).decode()
    while(clientsMessage != "EXIT"):
        splitMessage = clientsMessage.split(",")
        if(splitMessage[0] == "G"):
            groupMessage(splitMessage[1])
        elif(splitMessage[0] == "P"):
            clientIndex = clientNames.index(splitMessage[0])
            client.send(("123123," + clientIP[clientIndex][0] + "," + str(clientPorts[clientIndex])).encode())
            clientsMessage = ""
            
        

def groupMessage(message):
    for individual in clients:
        individual.send(message.encode())
        
connectToClients()