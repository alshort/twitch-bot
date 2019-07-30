"""
Main program entry point
"""
import sys

import bot

def main():
    """
    Runs the bot
    """
    qbot = bot.Bot()
    qbot.start()

    try:
        qbot.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()
