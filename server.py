import threading
import socket


host='127.0.0.1'#local host

port=55555

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
nickNames=[]

def broadCast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadCast(message)
        except:
            index=client.index(client)
            client.remove(client)
            nickname=nickNames[index]
            broadCast(f'{nickname} left the chat'.encode('ascii'))
            nickNames.remove(nickname)
            break
            
            
def receive():
    while True:
        client,address=server.accept()
    #print("connected with {(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        nickNames.append(nickname)
        clients.append(client)
        
        print(f'Nick name of the client is {nickname}')
        broadCast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to the server!!'.encode('ascii'))
        
        thread=threading.Thread(target=handle,args=(client,))
        thread.start()            
            
            
print("server is listing .....")
receive()
