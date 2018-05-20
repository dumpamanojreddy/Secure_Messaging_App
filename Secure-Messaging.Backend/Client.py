#!/usr/bin/python

import requests
import sys

REQUIRED_ARGUMENTS = 1

def main():
    # Minus one to account for system's default script path argument.
    argCount = len(sys.argv) - 1
    if argCount == REQUIRED_ARGUMENTS:
            url = str(sys.argv[1])
            run(url)
    else:
        print >> sys.stderr, "Wrong number of arguments, given {0} requires {1}".format(argCount, REQUIRED_ARGUMENTS)
        print >> sys.stderr, "Usage python Client.py http://<URL>:<PORT>"


def chat(token, url):
    exit = False
    while not exit:
        print "<Options>"
        print "0: Send Message"
        print "1: Get Messages"
        print "2: Get Conversations"
        print "3: See all users"
        print "4: Add a user as a friend"
        print "5: Show friends"
        print "6: Get Server's public key"
        print "7: Add my public key"
        print "8: Get users public key"
        print "9: Exit"

        option = raw_input("Choose: ")
        if option == '0':
            recipient = raw_input("Recipient: ")
            message = str(raw_input("Message: "))
            headers = {
                'token': token,
                'recipient': recipient
            }
            response = requests.post(url + '/sendMessage', data=message, headers=headers)
            if response.status_code == 200:
                print "{0} received your message!".format(recipient)
            else:
                print "{0} did not received your message...".format(recipient)
        elif option == '1':
            conversation = str(raw_input("Messages from? "))
            headers = {
                'token': token,
                'conversation': conversation
            }
            response = requests.get(url + '/getMessages', headers=headers)
            if response.status_code == 200:
                messages = response.json()['response']
                for message in messages:
                    print "{0}> {1}".format(message['sender'], message['message'])
            else:
                print "Something bad happened..."
        elif option == '2':
            headers = {'token': token}
            response = requests.get(url + '/getConversations', headers=headers)
            if response.status_code == 200:
                messages = response.json()['response']
                print messages
                # for message in messages:
                #     print "{0}> {1}".format(message['sender'], message['message'])
            else:
                print "Something bad happened..."
        elif option == "3":
            headers = {'token': token}
            response = requests.get(url + '/getUsers', headers=headers)
            if response.status_code == 200:
                users = response.json()['response']
                print users
        elif option == "4":
            friend = str(raw_input("Friend to add: "))
            headers = {
                'token': token,
                'friend': friend
            }
            response = requests.get(url + '/addFriend', headers=headers)
            if response.status_code == 200:
                response = response.json()['response']
                print response
        elif option == "5":
            headers = {'token': token}
            response = requests.get(url + '/getFriends', headers=headers)
            if response.status_code == 200:
                friends = response.json()['response']
                print friends
        elif option == "6":
            headers = {'token': token}
            response = requests.get(url + '/requestPublicKey', headers=headers)
            if response.status_code == 200:
                publicKey = response.json()['response']
                print publicKey
        elif option == "7":
            headers = {'publickey': 12}
            response = requests.post(url + '/setHandshakeKey', headers=headers)
            if response.status_code == 200:
                setHandshakeKey = response.json()['response']
                print setHandshakeKey
        elif option == "8":
            username = str(raw_input("Username who's public key you want: "))
            headers = {
                'token': token,
                'username': username
            }
            response = requests.get(url + '/getUsersPublicKey', headers=headers)
            if response.status_code == 200:
                usersPublicKey = response.json()['response']
                print usersPublicKey
        elif option == '9':
            exit = True

def login(url):
    failures = 0
    while failures < 3:
        print "You need to login..."
        username = raw_input("Username: ")
        password = raw_input("Password: ")
        publickey = 8675309
        privatekey = 60652
        if username != None and password != None:
            headers = {
                'username': username,
                'password': password,
                'publickey': publickey,
                'privatekey': privatekey
            }
            response = requests.post(url + '/login', data=None, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    print "You've logged in successfully!"
                    return data['token']
                return None
            else:
                print "You failed to login..."
                failures += 1


def run(url):
    token = login(url)
    if token != None:
        chat(token, url)

if __name__ == '__main__':
    main()