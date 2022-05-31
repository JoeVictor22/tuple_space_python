import random
from datetime import datetime
from typing import List, Dict, Set

import Pyro4

from config import PYRO_URL

import time

from app.tuple_object import TupleObject


class Client:
    broker = None

    name = None
    topics = None
    broker_topics = None

    buffer: List[Dict] = []
    rooms: Set[str] = set()
    messages: List[str] = []

    counter = None

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
        if now - self.counter < 0.16:
            return

        # Fetch room messages
        tuples = self.fetch_new_tuples(TupleObject(chat_room=self.room))
        for tuple in tuples:
            self.register_room(tuple)
            self.register_message(tuple)

        # Fetch private messages
        tuples = self.fetch_new_tuples(TupleObject(dest=self.name))
        for tuple in tuples:
            self.register_message(tuple)

    def register_room(self, tuple):
        if tuple['chat_room']:
            self.rooms.add(tuple['chat_room'])

    def register_message(self, tuple):
        self.messages.append(Client.format_message(tuple))

    def send_message(self, message, room=None, target=None):
        self.server.write(TupleObject(who=self.name,message=message, chat_room=room, dest=target))

    def get_participants(self):
        tuples = self.server.scan(TupleObject(chat_room=self.room))
        participants = set()

        for tuple in tuples:
            participants.add(tuple['who'])
        return list(participants)

    def fetch_new_tuples(self, tuple=TupleObject()):
        tuples = self.server.scan(tuple)
        if len(tuples) == 0:
            return []

        tuples: List[dict] = sorted(tuples, key=lambda x: x['sent_at'])
        tuples = list(filter(lambda x: x['sent_at'] > self.last_seen, tuples))

        if len(tuples) == 0:
            return []
        self.last_seen = tuples[-1]['sent_at']
        return tuples

    @staticmethod
    def format_message(tuple):

        time = datetime.fromtimestamp(tuple['sent_at']).strftime("%H:%M:%S")
        target = tuple['dest'] or tuple['chat_room']
        return f"[{time}]{tuple['who']}@{target} :  {tuple['message']}"
