"""
QwanderyBot
"""

import configparser
import re
import sys
import time

import requests

import irc


class Bot(object):
    def __init__(self):
        self.load_config()

        self.irc = irc.IrcClient("irc.twitch.tv", 6667)
        self.rate = float(20) / float(30)

        self.regexes = {
            "chat_message" : r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :"
        }

        self.commands = {
            "!shutdown" : self.shutdown,
            "!title" : self.get_title
        }

        """
        User goes to https://api.twitch.tv/kraken/oauth2/authorize?
        response_type=token&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=channel_editor

        self.client_id = "..."
        self.client_secret = "..."
        self.token = "..."
        """

    def load_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.client_id = config["twitch"]["client_id"]
        print(self.client_id)
        self.client_secret = config["twitch"]["client_secret"]
        print(self.client_secret)
        self.token = config["twitch"]["token"]
        print(self.token)

        self.channel = config["bot"]["channel"]
        print(self.channel)
        self.nick = config["bot"]["nick"]
        print(self.nick)
        self.password = config["bot"]["password"]
        print(self.password)

    def get_title(self, data):
        print("In get_title")
        url = "https://api.twitch.tv/kraken/channels/USERNAME"

        if data == None:
            # Get channel title
            print("Getting title...")
            resp = requests.get(url,
                headers={'Authorization': "OAuth " + self.token})

            if resp.status_code == 200:
                resp = resp.json()
                self.irc.chat(resp["status"])
            else:
                print(resp.status_code)
                print(resp)
        else:
            # Set channel title
            oauth = "OAuth " + self.token
            print(oauth)
            resp =  requests.put(url, {
                        "channel[status]" : data
                    },
                    headers={'Authorization': oauth})
            print(resp.status_code)

    def shutdown(self, data):
        self.irc.chat("Shutting down...")
        sys.exit(0)

    def start(self):
        print("Starting...")
        self.irc.connect(self.channel, self.nick, self.password)

    def run(self):
        print("Running...")

        chat_message = re.compile(self.regexes["chat_message"])

        while True:
            response = self.irc.response()
            if response == "PING :tmi.twitch.tv\r\n":
                self.irc.pong()
            else:
                username = re.search(r"\w+", response).group(0) # return the entire match
                message = chat_message.sub("", response)

                username = username.strip()
                message = message.strip()

                if message[0] == '!':
                    command_and_data = message.split(' ', 1)
                    command = command_and_data[0]

                    print(command_and_data)

                    if len(command_and_data) == 1:
                        data = None
                    else:
                        data = command_and_data[1]

                print(username)
                print(message)

                if username.lower() == "USERNAME":
                    try:
                        if command in self.commands:
                            print("Executing command " + command)
                            self.commands[command](data)
                    except NameError:
                        pass

                if message.lower() == "hi BOT_NAME":
                    print("match!")
                    self.irc.chat("Hello %s!" % username)

            time.sleep(1 / self.rate)
