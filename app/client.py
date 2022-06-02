import random
from datetime import datetime
from typing import List, Dict, Set

import Pyro4

from config import PYRO_URL

import time

from app.objects import TupleObject
#a

class Client:
    server = None

    name = None
    topics = None
    broker_topics = None

    buffer = []
    rooms = set()
    messages = []

    counter = None

    messages_id = []

    def __init__(self, room='default', name=None):
        if name is None:
            name = f"cliente_{random.randint(1000, 9999)}"

        self.last_seen = 0
        self.name = name
        self.room = room
        self.server = Pyro4.core.Proxy(PYRO_URL)
        self.counter = time.time()

    def update(self):
        now = time.time()
        if now - self.counter < 3:
            return

        msgs_on_server = self.server.scan(TupleObject(chat_room=self.room).pickled())
        private_msgs = self.server.scan(TupleObject(dest=self.name).pickled())
        global_msgs = self.server.scan(TupleObject().pickled())
        self.add_messages_to_buffer(msgs_on_server)
        self.add_messages_to_buffer(private_msgs)
        self.add_messages_to_buffer(global_msgs)

    def get_participants(self):
        return ["jose", "maria"]

    def _exists_in_client(self, message):
        if message in self.messages_id:
            return True
        return False

    def _add_new_message(self, message):
        if not message.uuid:
            return

        self.messages.append(message)
        self.messages_id.append(message.uuid)

        return message

    def add_messages_to_buffer(self, messages):
        msgs = map(TupleObject.pickle_deserialize, messages)
        added_msgs = [self._add_new_message(msg) for msg in msgs if not self._exists_in_client(msg)]

    @staticmethod
    def format_message(tuple):

        time = datetime.fromtimestamp(tuple['sent_at']).strftime("%H:%M:%S")
        target = tuple['dest'] or tuple['chat_room']
        return f"[{time}]{tuple['who']}@{target} : {tuple['message']}"
