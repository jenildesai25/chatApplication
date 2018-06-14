# Name : Jenil Bimal Desai
# UTA ID: 1001520245

# Citasions / References:
# https://stackoverflow.com/questions/37016946/remove-b-character-do-in-front-of-a-string-literal-in-python-3
# https://stackoverflow.com/questions/28271051/datetime-to-date-format-in-python
# https://stackoverflow.com/questions/12362542/python-server-only-one-usage-of-each-socket-address-is-normally-permitted

import json
from datetime import datetime


class ClientHelper:
    # encode client message and send it.
    def encodemessage(self, request):

        body = {'message': request}
        body_string = json.dumps(body)
        method = 'POST '
        host = 'JD'
        url = '/chat '
        protocol = 'HTTP/1.1'
        user_agent = 'Chat Room'
        content_type = 'application/json'
        content_length = len(body)
        date = datetime.utcnow().strftime('%a , %d  %b %Y %H:%M:%S GMT')

        header = method + url + protocol + "\r\n" + 'Host: ' + host + "\r\n" + 'User-Agent: ' + user_agent + "\r\n" \
                 + 'Content-Type: ' + content_type + "\r\n" + 'Content-Length: ' + str(content_length) + "\r\n" + \
                 'Date: ' + date

        encodedMessage = header + "\r\n\r\n" + body_string

        return encodedMessage
