from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("192.168.56.1", serverPort))
serverSocket.listen(3)
print("The server is running...")

clientNames = []
clientIP = []
clientPorts = []
clients = []
clientsPrivacyStatus = []



def connectToClients():
    while True:
        client, addr = serverSocket.accept()
        print("Connected to", addr)
        client.send("NAME&PORT&PRIVACYSTATUS".encode())
        clientNameAndPort = client.recv(1024).decode()
        clientName = clientNameAndPort.split(",")[0]
        clientPort = clientNameAndPort.split(",")[1]
        clientPrivacyStatus = clientNameAndPort.split(",")[2]
        clientIP.append(addr)
        clientNames.append(clientName)
        clients.append(client)
        clientPorts.append(clientPort)
        clientsPrivacyStatus.append(clientPrivacyStatus)
        
        print("Connection successful.")
        
        thread = threading.Thread(target=temp, args =(client,))
        thread.start()

    
def temp(client):
    try:
        clientsMessage = client.recv(1024).decode()
        while(clientsMessage != "EXIT"):
            splitMessage = clientsMessage.split(",")
            if(splitMessage[0] == "G"):
                groupMessage(splitMessage[1], splitMessage[1].split(":")[0])
            elif(splitMessage[0] == "P"):
                try:
                    clientIndex = clientNames.index(splitMessage[1])
                    if(clientsPrivacyStatus[clientIndex] == "private"):
                        client.send("Error".encode())
                        continue
                except ValueError:
                    client.send("Error".encode())
                    continue
                client.send((clientIP[clientIndex][0] + "," + str(clientPorts[clientIndex])).encode())
            elif(splitMessage[0] == "L"):
                x = 0
                listOfAvailableClients = []
                for person in clientNames:
                    if(clientsPrivacyStatus[x] != "private"):
                        listOfAvailableClients.append(person)
                    x = x+1
                
                outputString = ""        
                for i, name in enumerate(listOfAvailableClients, 1):
                    outputString += f"{i}. {name}\n"
                client.send(outputString.encode())
            
            clientsMessage = client.recv(1024).decode()
    
    except ConnectionResetError:
        print("Client has disconnected")
        try:
            client_index = clients.index(client)
            del clients[client_index]
            del clientNames[client_index]
            del clientIP[client_index]
            del clientPorts[client_index]
            del clientsPrivacyStatus[client_index]
        except ValueError:
            pass  # Client not found in lists
        

def groupMessage(message , name):
    index = clientNames.index(name)
    i = 0
    for individual in clients:
        if(i != index):
            individual.send(("123123" + message).encode())
        i = i + 1
connectToClients()
