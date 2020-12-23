import threading

from bot_sylwester.client import run_discord_client
from bot_sylwester.server import run_server


def thread_handler_flask():
    run_server(2137)


if __name__ == "__main__":
    thread_flask = threading.Thread(target=thread_handler_flask)
    thread_flask.start()

    run_discord_client()
