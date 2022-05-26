import random

import Pyro4

from config import PYRO_URL

import time


class Chat:
    buttons = []
    forms = []
    texts = []

    def __init__(self):
        pass

    def update(self):
        now = time.time()
        if now - self.counter < 0.16:
            return

    @staticmethod
    def format_message(message):
        import time

        # from datetime import datetime
        # time = datetime.now().strftime("%H:%M:%S")
        time = time.time()
        return f"[{time}] - {message}"
