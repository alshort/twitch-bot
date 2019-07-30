import socket

class IrcClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.socket = socket.socket()

    def connect(self, channel, username, password):
        self.socket.connect((self.host, self.port))
        self.socket.send("PASS {}\r\n".format(password).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(username).encode("utf-8"))
        self.socket.send("JOIN {}\r\n".format(channel).encode("utf-8"))

        self.channel = channel

    def chat(self, msg):
        """
        Send a chat message to the server.
        Keyword arguments:
        msg  -- the message to be sent
        """
        self.socket.send('PRIVMSG %s :%s\n' % (self.channel, msg.encode('utf-8')))

    def ban(self, user):
        """
        Ban a user from the current channel.
        Keyword arguments:
        user -- the user to be banned
        """
        self.chat(".ban {}".format(user))

    def timeout(self, user, secs=600):
        """
        Time out a user for a set period of time.
        Keyword arguments:
        sock -- the socket over which to send the timeout command
        user -- the user to be timed out
        secs -- the length of the timeout in seconds (default 600)
        """
        self.chat(".timeout {} {}".format(user, secs))

    def response(self):
        return self.socket.recv(1024).decode("utf-8")

    def pong(self):
        self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
