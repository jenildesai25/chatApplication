# Name : Jenil Bimal Desai
# UTA ID: 1001520245

# Citasions / References:
# https://www.geeksforgeeks.org/simple-chat-room-using-python/
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
# https://stackoverflow.com/questions/21058935/python-json-loads-shows-valueerror-extra-data
# https://stackoverflow.com/questions/30921399/datetime-fromtimestamp-vs-datetime-utcfromtimestamp-which-one-is-safer-to-use
# https://regex101.com/
# https://stackoverflow.com/questions/41761084/attributeerror-type-object-socket-has-no-attribute-socket

import re
import json
import threading
import time
import socket
from threading import Thread
from Helper import Helper


def accept_incoming_connections():
    """ Sets up handling for incoming clients. """
    while True:
        client, client_address = server_socket.accept()
        # print("%s:%s has connected." % client_address)
        # it encodes the message from client and sent it to server.
        encoded_message = Helper().encodehttprequest(
            messsage="Greetings from the server! Now type your name and press enter!", timestamp=time.time())
        client.send(encoded_message.encode())
        addresses[client] = client_address
        # print(addresses.values())
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """ Handles a single client connection. """
    try:
        while 1:
            # server receives the message every time client sends it.
            name = client.recv(buffer_size).decode("utf8")
            msg_after_split = name.split('\r\n\r\n')
            body = json.loads(msg_after_split[1])
            name = body['message']
            # check the bad name here.
            if re.match('^[a-z A-Z]+$', name):
                break
            else:
                error_message = Helper().encodehttprequest(messsage='Only alphabets are allowed no number or special characters are allowed.', timestamp=time.time())
                client.send(error_message.encode())
        print(name, ':handles by', threading.current_thread())
        # print('body is: ', body)
        welcome = 'Welcome %s! If you ever want to quit, type quit to exit.' % body['message']
        # Use to generate response in HTTP format.
        print(Helper().encodehttprequest(messsage=welcome, timestamp=time.time()))
        encoded_message = Helper().encodehttprequest(messsage=welcome, timestamp=time.time())
        # print("Server Sent!!: ", encoded_message)
        client.send(encoded_message.encode())
        msg = "%s has joined the chat!" % name
        # print("\nPre Broadcast")
        broadcast(msg, name)
        # print("\nPost Broadcast")
        clients[client] = name
        while True:
            # used to receive message from client.
            msg = client.recv(buffer_size).decode()
            msg_after_split = msg.split('\r\n\r\n')
            body = json.loads(msg_after_split[1])
            # print("body receive at the server is: ", body)
            msg = body['message']
            # print("client name: ", clients.get(client))
            # print("Server Rec2", msg)
            if msg != "quit":
                # print("current source name is: ",)
                broadcast(msg, name, name + ": ")
            else:
                encoded_message = Helper().encodehttprequest(messsage='quit', timestamp=time.time())
                client.send(encoded_message.encode())
                client.close()
                del clients[client]
                broadcast("%s has left the chat." % name,name)
                break

    except OSError:
        pass
        # if someone left the chat it goes here.
        closed_connection_msg = ' has closed connection forcefully.'
        print(name, closed_connection_msg)
        file = open('log.txt', '+a')
        file.write(json.dumps({'name': name, 'message': closed_connection_msg}))
        file.write('\n')
        file.close()


def broadcast(msg, name, prefix=""):  # prefix is for name identification.
    """ Broadcasts a message to all the clients. """
    # print("message is received form broadcast: ", msg)
    # print("prefix at broadcast level: ", prefix)
    # write all the log to log.txt file.
    file = open('log.txt', '+a')
    file.write(json.dumps({'client_name': name, 'message': msg}))
    file.write('\n')
    file.close()
    for sock in clients:
        encoded_message = Helper().encodehttprequest(messsage=prefix + ' ({time}) - ' + msg, timestamp=time.time())
        # print("Server Broadcasted: ", encoded_message)
        sock.send(encoded_message.encode())


clients = {}
addresses = {}
# give host address of the server
host = 'JD'
# give port number of the server
port = 8080
# assign buffer size to store the data
buffer_size = 1024

# create socket to listen to client.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind host and port
# server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind((host, port))
# c = Client()
if __name__ == "__main__":
    server_socket.listen()
    print("Multi threaded python server has started.")
    restart_file = open('log.txt', 'r')
    lines = restart_file.readlines()
    for line in lines:
        print(line)
    print("Waiting for connection...\n")
    # thread has been initialized by upcoming statement.
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    print('thread has been created.')
    ACCEPT_THREAD.join()
    server_socket.close()

