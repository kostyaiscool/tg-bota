import threading

from api.__main__ import run_api
from bot.__main__ import start_bot

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    run_api()

    bot_thread.join()
