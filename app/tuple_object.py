import time
from dataclasses import dataclass
from uuid import uuid4 as UUID


@dataclass
class TupleObject:
    unique_id: str = str(UUID())
    sent_at: int = int(time.time())

    dest: str = None
    who: str = None
    chat_room: str = None
    message: str = None

    tuple_space_fields = ["chat_room", "dest", "who"]

    @classmethod
    def deserialize(cls, data):
        return cls(**data)

    def is_equal_to(self, tupla: object) -> object:

        for key in self.tuple_space_fields:
            is_self_none = getattr(self, key) is None
            is_other_none = getattr(tupla, key) is None
            are_different = getattr(tupla, key) != getattr(self, key)

            if not is_self_none and not is_other_none and are_different:
                return False
        return True
