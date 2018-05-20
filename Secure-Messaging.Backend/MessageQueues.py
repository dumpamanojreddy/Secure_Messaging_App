from Database import Database
import sys
import time

# A queue like data structure for holding a user's messages.
class MessageQueues:
    TABLE_CONVERSATIONS = 'Conversations'
    TABLE_FRIENDS = 'Friends'
    TABLE_MESSAGE_QUEUES = "MessageQueues"

    conversations = {}
    friends = {}
    queues = None

    @staticmethod
    def initMQ():
        MessageQueues.conversations = Database.get(MessageQueues.TABLE_CONVERSATIONS)
        MessageQueues.friends = Database.get(MessageQueues.TABLE_FRIENDS)
        MessageQueues.queues = Database.get(MessageQueues.TABLE_MESSAGE_QUEUES)

        if MessageQueues.conversations == None:
            Database.add(MessageQueues.TABLE_CONVERSATIONS, {})
            MessageQueues.conversations = Database.get(MessageQueues.TABLE_CONVERSATIONS)
        if MessageQueues.friends == None:
            Database.add(MessageQueues.TABLE_FRIENDS, {})
            MessageQueues.friends = Database.get(MessageQueues.TABLE_FRIENDS)
        if MessageQueues.queues == None:
            Database.add(MessageQueues.TABLE_MESSAGE_QUEUES, {})
            MessageQueues.queues = Database.get(MessageQueues.TABLE_MESSAGE_QUEUES)

    @staticmethod
    def add(username, sender, message, iv):
        if username != None:
            message = {
                    'sender': sender,
                    'message': message,
                    'iv' : iv,
                    'timestamp': int(time.time())
                }
            if username in MessageQueues.queues:
                messages = MessageQueues.queues[username]
                messages.append(message)
            else:
                MessageQueues.queues[username] = [message]
            # Create conversations. One call will make conversations for both the user and sender.
            MessageQueues.addConversation(username, sender)
        else:
            print >> sys.stderr, "Username is None"

    @staticmethod
    def addConversation(username, sender, createForSender=True):
        if username in MessageQueues.conversations:
            conversations = MessageQueues.conversations[username]
            if sender not in conversations:
                conversations.append(sender)
        else:
            MessageQueues.conversations[username] = [sender]
        # Create conversation for the sender as well.
        if createForSender:
            MessageQueues.addConversation(sender, username, False)
        print MessageQueues.conversations


    @staticmethod
    def addFriends(username, friend):
        if username in MessageQueues.friends:
            friends = MessageQueues.friends[username]
            if friend not in friends:
                friends.append(friend)
                print friends
        else:
            MessageQueues.friends[username] = [friend]

    @staticmethod
    def getMessages(username, sender, getSenderMessages=True):
        messages = []
        if username != None and username in MessageQueues.queues:
            userMessages = MessageQueues.queues[username]
            for message in userMessages:
                if message['sender'] == sender:
                    messages.append(message)
        if getSenderMessages:
            messages += MessageQueues.getMessages(sender, username, False)
        
        return sorted(messages, key=lambda message: message['timestamp'])

    @staticmethod
    def getConversations(username):
        conversations = MessageQueues.conversations
        if username != None and username in conversations:
            return conversations[username]
        else:
            return []

    @staticmethod
    def getFriends(username):
        friends = MessageQueues.friends
        if username != None and username in friends:
            return friends[username]
        else:
            return []

