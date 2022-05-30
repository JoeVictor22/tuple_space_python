from config import PYRO_URL

if __name__ == "__main__":
    import Pyro4

    with Pyro4.Proxy(PYRO_URL) as p:
        try:
            p._pyroBind()



            from app.client import Client

            print("Criando Cliente")
            # name = input("Digite o seu nome (vazio para gerar aleatorio)\n")

            # if name == "":
            #     name = None

            from app.chat_interface import Interface
            a = Interface().start()

        except Pyro4.errors.CommunicationError as eee:
            from app.server import start_server

            print(eee)

            print("Iniciando servidor")
            start_server()
