import random

import Pyro4

from config import PYRO_URL

import time


class Client:
    broker = None

    name = None
    topics = None
    broker_topics = None
    buffer = None
    counter = None

    def __init__(self, name=None):
        if name is None:
            name = f"cliente_{random.randint(1000,9999)}"

        self.buffer = list()
        self.insert_message(f"[Iniciando cliente] {name}")
        self.topics = list()
        self.name = name
        self.value = random.randint(0, 400)
        self.broker = Pyro4.core.Proxy(PYRO_URL)
        self.broker_topics = list()

    def set_topics(self, new_topics):
        self.topics = new_topics

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
