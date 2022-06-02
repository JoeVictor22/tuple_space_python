# tuple_space_python

## Como executar
```shell
python main.py
```

	from config import PYRO_URL
import Pyro4


from app.objects import TupleObject
import pickle

server = Pyro4.core.Proxy(PYRO_URL)



def send(vai):
    b =  pickle.dumps(vai)
    server.write(b)



a = TupleObject(dest="joao", who="joel", chat_room="default", message="hola")
send(a)
a.who="jose"
send(a)
a.chat_room="not_default"
send(a)
a.dest("joaquim")
send(a)
a.who =None
a.chat_room = None
send(a)
a.who = "joel"
send(a)
a.chat_room="not_default"
send(a)