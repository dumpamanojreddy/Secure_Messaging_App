from collections import namedtuple
from Database import Database
from MessageQueues import MessageQueues

import base64
import CBC
import hashlib
import random
import time
import json


class EverythingHandler:
    P = 1255049
    BASE = 113359
    BIG_INTEGER = 2147483647
    TABLE_USER_CREDENTIALS = "UserCredentials"

    SUCCESS = 0
    RESPONSE = 1

    serversPrivateKey = None
    serversPublicKey = None

    AuthRecord = namedtuple('AuthRecord', ['username', 'password'])
    Message = namedtuple('Message', ['sender', 'message', 'iv'])

    authTable = {}
    messageTable = {}
    tempHandShakeTable = {}

    Database.initDB()
    MessageQueues.initMQ()

    @staticmethod
    def authenticateRequest(headers):
        if 'token' in headers:
            token = headers['token']
            if token in EverythingHandler.authTable:
                return True
        return False

    @staticmethod
    def addFriend(headers):
        if EverythingHandler.authenticateRequest(headers):
            token = headers['token']
            friend = headers['friend']
            username = EverythingHandler.getUsernameByToken(token)
            MessageQueues.addFriends(username, friend)
            return True, {"response": EverythingHandler.getPublicKey(friend)}
        return False, None

    @staticmethod
    def checkUserIsReal(username):
        # Look up user in a database table.
        return username != None and username in Database.get(EverythingHandler.TABLE_USER_CREDENTIALS)

    @staticmethod
    def getMessages(headers):
        if EverythingHandler.authenticateRequest(headers):
            token = headers['token']
            conversation = headers['conversation']
            username = EverythingHandler.getUsernameByToken(token)
            return True, {"response": MessageQueues.getMessages(username, conversation)}
        return False, None

    @staticmethod
    def getConversations(headers):
        if EverythingHandler.authenticateRequest(headers):
            token = headers['token']
            username = EverythingHandler.getUsernameByToken(token)
            return True, {"response": MessageQueues.getConversations(username)}
        return False, None


    @staticmethod
    def getFriends(headers):
        if EverythingHandler.authenticateRequest(headers):
            token = headers['token']
            username = EverythingHandler.getUsernameByToken(token)
            return True, {"response": MessageQueues.getFriends(username)}
        return False, None

    @staticmethod
    def getToken(record):
        tokenString = "{0}{1}{2}".format(record.username, record.password, int(time.time()))
        tokenRaw = hashlib.sha512(tokenString).digest()
        tokenBase64 = base64.b64encode(tokenRaw)
        return tokenBase64

    @staticmethod
    def getUsers(headers):
        if EverythingHandler.authenticateRequest(headers):
            userCreds = Database.get(EverythingHandler.TABLE_USER_CREDENTIALS)
            users = []
            for user in userCreds:
                users.append(user)
            return True, {"response": users}
        return False, None

    @staticmethod
    def getUsersPublicKey(headers):
        if EverythingHandler.authenticateRequest(headers):
            if 'username' in headers:
                username = headers['username']
                usersPublicKey = EverythingHandler.getPublicKey(username)
                return True, {"response": usersPublicKey}
        return False, None

    @staticmethod
    def getPublicKey(username):
        if EverythingHandler.checkUserIsReal(username):
            userCreds = Database.get(EverythingHandler.TABLE_USER_CREDENTIALS)
            creds = userCreds[username]
            publickey = creds['publickey']
            if publickey == None:
                EverythingHandler.generateClientKeys(username)
            return creds['publickey']
        return None

    @staticmethod
    def generateClientKeys(username):
        if EverythingHandler.checkUserIsReal(username):
            userCreds = Database.get(EverythingHandler.TABLE_USER_CREDENTIALS)
            creds = userCreds[username]

            if creds['publickey'] == None  or creds['privatekey'] == None:
                privatekey = random.randint(2, EverythingHandler.P - 2)
                publickey = pow(EverythingHandler.BASE, privatekey, EverythingHandler.P)
                creds['publickey'] = publickey
                creds['privatekey'] = privatekey
                userCreds[username] = creds
            return {'publickey': creds['publickey'], 'privatekey': creds['privatekey']}
        return None


    @staticmethod
    def getUsernameByToken(token):
        if token in EverythingHandler.authTable:
            return EverythingHandler.authTable[token].username
        return None

    @staticmethod
    def login(headers, body):
        if 'username' in headers and 'password' in headers and 'tempHandshakeID' in headers and 'iv' in headers:
            username = str(headers['username']).lower()
            iv = json.loads(headers['iv'])
            tempHandshakeID = int(headers['tempHandshakeID'])
            key = EverythingHandler.tempHandShakeTable[tempHandshakeID]
            encryptedPass = json.loads(headers['password'])
            password = CBC.AESdecrypt(json.loads(headers['password']), key['sharedkey'], iv)
            if EverythingHandler.matchCreds(username, password):
                # TODO: Hash the password!
                record = EverythingHandler.AuthRecord(username, password)
                token = EverythingHandler.getToken(record)
                EverythingHandler.authTable[token] = record
                clientKeys = EverythingHandler.generateClientKeys(username)
                encryptedData = CBC.AESencrypt(str(clientKeys['privatekey']), key['sharedkey'])
                print "{0} has logged on with token: {1}".format(username, token)
                print "Client keys are {0}".format(clientKeys)
                return True, {'token': token, 'privateKey': encryptedData[0], "iv" : encryptedData[1] }
        return False, None

    # Preset database of creds.
    @staticmethod
    def matchCreds(username, password):
        userCredentials = Database.get(EverythingHandler.TABLE_USER_CREDENTIALS)
        # If the User Credentials table is empty set up some default info.
        if userCredentials == None:
            Database.add(EverythingHandler.TABLE_USER_CREDENTIALS, {
                'omkar': {'password': hashlib.sha1('omkar').hexdigest(), 'publickey': None, 'privatekey': None},
                'manoj': {'password': hashlib.sha1('manoj').hexdigest(), 'publickey': None, 'privatekey': None},
                'rohan': {'password': hashlib.sha1('rohan!').hexdigest(), 'publickey': None, 'privatekey': None}
            })
            userCredentials = Database.get(EverythingHandler.TABLE_USER_CREDENTIALS)

        username = str(username).lower()
        if username in userCredentials:
            return userCredentials[username]['password'] == password
        else:
            userCredentials[username] = {'password': password, 'publickey': None, 'privatekey': None}
            return True


    @staticmethod
    def sendMessage(headers, body):
        if EverythingHandler.authenticateRequest(headers):
            if 'recipient' in headers:
                recipient = headers['recipient']
                if EverythingHandler.checkUserIsReal(recipient):
                    token = headers['token']
                    iv = headers['iv']
                    sender = EverythingHandler.getUsernameByToken(token)
                    message = EverythingHandler.Message(sender, body, iv)
                    MessageQueues.add(recipient, sender, body, iv)
                    return True, {"response": "sent"}
        else:
            return False, None


    @staticmethod
    def requestPublicKey():
        if EverythingHandler.serversPublicKey == None:
            EverythingHandler.generateKeys()
        response = {
            "publickey": EverythingHandler.serversPublicKey,
            "p": EverythingHandler.P,
            "base": EverythingHandler.BASE
        }
        return True, {"response": response}


    @staticmethod
    def setHandshakeKey(headers):
        if 'publickey' in headers:
            # Generate a unique temporary id for this session
            tempHandshakeID = random.randint(0, EverythingHandler.BIG_INTEGER)
            while tempHandshakeID in EverythingHandler.tempHandShakeTable:
                tempHandshakeID = random.randint(0, EverythingHandler.BIG_INTEGER)

            publicKey = int(headers['publickey']) 
            sharedKey = EverythingHandler.generateSharedKey(publicKey)
            keys = {
                'publickey': publicKey,
                'sharedkey': sharedKey
            }
            EverythingHandler.tempHandShakeTable[tempHandshakeID] = keys
            return True, {"response": tempHandshakeID}
        return False, None


    @staticmethod
    def generateKeys():
        #privateKey = random.randint(2, EverythingHandler.P - 2)
        privateKey = 670570;
        publicKey = pow(EverythingHandler.BASE, privateKey, EverythingHandler.P)
        EverythingHandler.serversPrivateKey = privateKey
        EverythingHandler.serversPublicKey = publicKey

    @staticmethod
    def generateSharedKey(publickey):
        s = pow(publickey, EverythingHandler.serversPrivateKey, EverythingHandler.P)

        s = hashlib.sha1(str(s)).hexdigest()

        i = 0
        key = []
        while i < 32:
            key += [int(s[i:i+2], 16)]
            i += 2
        return key