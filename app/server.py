from copy import deepcopy
import Pyro4

from app.objects import TupleObject
from typing import List


@Pyro4.expose
class Servidor(object):
    tuple_space: List[TupleObject] = list()

    def _search_for_tuples(self, tupla: TupleObject):
        yield from filter(lambda obj: tupla.is_equal_to(obj), self.tuple_space)

    def write(self, tupla: TupleObject):
        if not isinstance(tupla, TupleObject):
            return

        self.tuple_space.append(tupla)

    def take(self, tupla: TupleObject):
        if not isinstance(tupla, TupleObject):
            return

        next_tuple = next(self._search_for_tuples(tupla))
        tuple_found = deepcopy(next_tuple)
        self.tuple_space.remove(next_tuple)
        return tuple_found

    def read(self, tupla: TupleObject):
        if not isinstance(tupla, TupleObject):
            return

        next_tuple = next(self._search_for_tuples(tupla))
        return next_tuple

    def scan(self, tupla: TupleObject):
        if not isinstance(tupla, TupleObject):
            return

        tuples = list(self._search_for_tuples(tupla))
        return tuples

    def count(self, tupla: TupleObject):
        if not isinstance(tupla, TupleObject):
            return

        tuples = list(self._search_for_tuples(tupla))
        return len(tuples)


def start_server():
    Pyro4.Daemon.serveSimple(
        {
            Servidor: "Server",
        },
        host="0.0.0.0",
        port=9090,
        ns=False,
        verbose=True,
    )
    print(f"[Server started]")
