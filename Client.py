# Name : Jenil Bimal Desai
# UTA ID: 1001520245

# Citasions / References:
# http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# https://www.daniweb.com/programming/software-development/threads/481619/server-split-message-and-save-data-on-a-text-file
# http://codingnights.com/coding-fully-tested-python-chat-server-using-sockets-part-1/
# https://stackoverflow.com/questions/18685184/pep8-e501-line-too-long-error

import json
import sys
import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import messagebox

from Client_helper import ClientHelper


def receive():
    """Handles receiving of messages."""
    _last_time = 0
    while True:
        try:
            # receive message from server.
            msg = client_socket.recv(buffer_size).decode("utf8")
            # print('msg received: ', msg)
            # split the header and body.
            msg_after_split = msg.split('\r\n\r\n')
            body = json.loads(msg_after_split[1])
            # print('body is: ', body)
            # count the time difference between 2 chats.
            if _last_time == 0:
                _last_time = body['time']
            time_passed = body['time'] - _last_time
            m, s = divmod(time_passed, 60)
            h, m = divmod(m, 60)
            body['message'].format(time="%d:%02d" % (m, s))
            msg_list.insert(tkinter.END, body['message'].format(time="%d:%02d" % (m, s)))
            _last_time = body['time']
        except OSError:  # Possibly client has left the chat.
            sys.exit()


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field
    encoded_message = ClientHelper().encodemessage(msg)
    client_socket.send(encoded_message.encode())
    if msg == "quit":
        client_socket.close()
        top.destroy()
        top.quit()


def on_closing():
    """This function is to be called when the window is closed."""
    # ask to close the application.
    if tkinter.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        top.destroy()
        encoded_message = ClientHelper().encodemessage('has left the chat.')
        client_socket.send(encoded_message.encode())
        client_socket.close()
    else:
        pass


# create instace of the tkinter.
top = tkinter.Tk()
top.title("Chat Room")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# Socket and port name is defined and thread starts from here.

host = 'JD'
port = 8080
address = (host, port)
buffer_size = 1024
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
