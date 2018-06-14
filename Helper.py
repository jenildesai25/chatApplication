# Name : Jenil Bimal Desai
# UTA ID: 1001520245

# Citasions / References:
# https://stackoverflow.com/questions/17501131/sending-txt-file-to-server-from-client-using-python-sockets
# https://stackoverflow.com/questions/7408647/convert-dynamic-python-object-to-json

from datetime import datetime
from json import dumps


class Helper:
    # encode the request and send it.
    def encodehttprequest(self, messsage, timestamp):
        body = {'message': messsage, 'time': timestamp}
        body_str = dumps(body)
        method = "POST"
        contentType = "application/json; " + '\n' + "Accept-charset = UTF-8"
        userAgent = "Chat Room"
        host = 'JD'
        contentlength = len(body_str)
        date = date = datetime.utcnow().strftime('%a , %d  %b %Y %H:%M:%S GMT')

        titleheader = 'HTTP/1.1 200 OK\r\n'

        headers = method + ' ' + titleheader + "Host: " + host + '\r\n' + "Content-Length: " + str(contentlength) + "\r\n" + "User-Agent: " + \
                  userAgent + "\r\n" + "Content-Type: " + contentType + '\r\n' +  'Date: ' + date

        encodedMessage = headers + "\r\n\r\n" + body_str

        return encodedMessage


