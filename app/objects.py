from dataclasses import dataclass
from uuid import uuid1 as UUID

from typing import List


@dataclass
class TupleObject:
    unique_id: UUID
    dest: str
    who: str
    chat_room: str
    message: str

    tuple_space_fields = ["chat_room", "dest", "who"]

    def __new__(cls):
        unique_id = UUID()
        return super().__new__(cls, unique_id)

    def is_equal_to(self, tupla):
        for key in self.tuple_space_fields:
            if getattr(self, tupla) and getattr(self, key) != getattr(self, tupla):
                return False
        return True
