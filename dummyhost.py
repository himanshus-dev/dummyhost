#/usr/bin/python3
'''DummyHost - A dummy HTTP REST API server
Usage:
    dummyhost <port> [--schema=<FILE>]

Options:
    -h --help       Show this screen.
    -v --version    Show version.
'''
import sys
import json
from docopt import docopt
from schema import Schema, And, Or, Use, SchemaError
from http.server import HTTPServer, BaseHTTPRequestHandler

# define jsonfile name
jsonfile = "example.json"

#Defining a HTTP request Handler class
class DummyHostCustomServiceHandler(BaseHTTPRequestHandler):

    # sets basic headers for the server
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        # reads the length of the Headers
        length = int(self.headers['Content-Length'])
        # reads the contents of the request
        content = self.rfile.read(length)
        temp = str(content).strip('b\'')
        self.end_headers()
        return temp

    # GET Method Defination
    def do_GET(self):
        # find the endpoint requested
        endpoint_json = self.get_endpoint_json(self.path)
        # print(self.path)
        if endpoint_json :
            # defining all the headers
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            # prints all the keys and values of the json file
            self.wfile.write(json.dumps(endpoint_json['GET']).encode())
        else :
            # defining all the headers
            self.send_response(404)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            # # prints all the keys and values of the json file
            self.wfile.write(json.dumps({"msg":"Endpoint not found."}).encode())

    # POST method defination
    def do_POST(self):
        temp = self._set_headers()
        key = 0
        # getting key and value of the data dictionary
        for key, value in data.items():
            pass
        index = int(key)+1
        data[str(index)] = str(temp)
        # write the changes to the json file
        with open(jsonfile, 'w+') as file_data:
            json.dump(data, file_data)
        # self.wfile.write(json.dumps(data[str(index)]).encode())

    # PUT method Defination
    def do_PUT(self):
        temp = self._set_headers()
        # seprating input into key and value
        x = temp[:1]
        y = temp[2:]
        # check if key is in data
        if x in data:
            data[x] = y
            # write the changes to file
            with open("db.json", 'w+') as file_data:
                json.dump(data, file_data)
            # self.wfile.write(json.dumps(data[str(x)]).encode())
        else:
            error = "NOT FOUND!"
            self.wfile.write(bytes(error, 'utf-8'))
            self.send_response(404)
    
    # Method for searching endpint in json
    def get_endpoint_json(self, path):
        for element in data:
            if element['endpoint'] == path :
                return element
        return None


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Dummy Host 1.0')

    #open json file and give it to data variable as a dictionary
    jsonfile = arguments['--schema']
    with open(jsonfile) as data_file:
        data = json.load(data_file)
    
    # HTTP Server Initialization
    server_address = ('', int(arguments['<port>']))
    httpd = HTTPServer(server_address, DummyHostCustomServiceHandler)
    httpd.serve_forever()
