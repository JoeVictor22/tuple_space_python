import dataclasses

import Pyro4

from app.tuple_object import TupleObject

Pyro4.util.SerializerBase.register_class_to_dict(TupleObject, dataclasses.asdict)

from config import PYRO_URL

if __name__ == "__main__":

    with Pyro4.Proxy(PYRO_URL) as p:
        try:
            p._pyroBind()



            from app.client import Client

            print("Criando Cliente")
            name = input("Digite o seu nome\n")

            if name == "":
                name = "joao"

            from app.chat_interface import Interface
            a = Interface(name=name).start()

        except Pyro4.errors.CommunicationError as eee:
            from app.server import start_server

            print(eee)

            print("Iniciando servidor")
            start_server()
