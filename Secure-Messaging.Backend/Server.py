#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from EverythingHandler import EverythingHandler
import json
import ssl
import sys

REQUIRED_ARGUMENTS = 2

def main():
    # Minus one to account for system's default script path argument.
    argCount = len(sys.argv) - 1
    if argCount == REQUIRED_ARGUMENTS:
        try:
            port = int(sys.argv[1])
            enableSSL = makeBool(sys.argv[2])
            if enableSSL == True:
                print 'good'
            if port <= 65535:
                run(port, enableSSL)
            else:
                print >> sys.stderr, "Port out of range 1 to 65535."
        except Exception as e:
            print >> sys.stderr,  e.message
    else:
        print >> sys.stderr, "Wrong number of arguments, given {0} requires {1}".format(argCount, REQUIRED_ARGUMENTS)
        print >> sys.stderr, "Usage: python Server.py <PORT> <enableSSL>"


def makeBool(string):
    return str(string).lower() == 'true'


def run(port, enableSSL):
    server = None
    try:
        server = HTTPServer(('', port), DummyHandler)
        if enableSSL == True:
            server.socket = ssl.wrap_socket(server.socket, 'server.key', server_side=True)
            print 'SSL enabled use HTTPS.'
        print 'Started httpserver on port', port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
    except Exception as e:
        print >> sys.stderr, e.message
        server.socket.close()


class DummyHandler(BaseHTTPRequestHandler):
    EverythingHandler.generateKeys()
    def do_GET(self):
        if self.path == '/addFriend':
            addFriend = EverythingHandler.addFriend(self.headers)
            if addFriend[EverythingHandler.SUCCESS]:
                self.respondGood(addFriend[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/getUsersPublicKey':
            getUsersPublicKey = EverythingHandler.getUsersPublicKey(self.headers)
            if getUsersPublicKey[EverythingHandler.SUCCESS]:
                self.respondGood(getUsersPublicKey[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/getConversations':
            getConversations = EverythingHandler.getConversations(self.headers)
            if getConversations[EverythingHandler.SUCCESS]:
                self.respondGood(getConversations[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/getFriends':
            friends = EverythingHandler.getFriends(self.headers)
            if friends[EverythingHandler.SUCCESS]:
                self.respondGood(friends[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/getMessages':
            getMessages = EverythingHandler.getMessages(self.headers)
            if getMessages[EverythingHandler.SUCCESS]:
                self.respondGood(getMessages[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/requestPublicKey':
            requestPublicKey = EverythingHandler.requestPublicKey()
            if requestPublicKey[EverythingHandler.SUCCESS]:
                self.respondGood(requestPublicKey[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/getUsers':
            getUsers = EverythingHandler.getUsers(self.headers)
            if getUsers[EverythingHandler.SUCCESS]:
                self.respondGood(getUsers[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        else:
            self.respondBad()
        return

    def do_POST(self):
        if self.path == '/login':
            login = EverythingHandler.login(self.headers, self.readRequest())
            if login[EverythingHandler.SUCCESS]:
                self.respondGood(login[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/sendMessage':
            sendMessage = EverythingHandler.sendMessage(self.headers, self.readRequest())
            if sendMessage[EverythingHandler.SUCCESS]:
                self.respondGood(sendMessage[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        elif self.path == '/setHandshakeKey':
            setHandshakeKey = EverythingHandler.setHandshakeKey(self.headers)
            if setHandshakeKey[EverythingHandler.SUCCESS]:
                self.respondGood(setHandshakeKey[EverythingHandler.RESPONSE])
            else:
                self.respondBad()
        else:
            self.respondBad()
        return

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")

    def readRequest(self):
        length = int(self.headers['Content-Length'])
        return self.rfile.read(length).decode('utf-8')

    def respondGood(self, response):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(json.dumps(response))

    def respondBad(self):
        self.send_response(400)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write("Something bad happened...\n")



if __name__ == '__main__':
    main()