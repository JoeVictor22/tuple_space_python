from config import PYRO_URL

if __name__ == "__main__":
    import Pyro4

    with Pyro4.Proxy(PYRO_URL) as p:
        try:
            p._pyroBind()

            choice = input(
                "Digite: \n1 (para criar um cliente)\n2 (para criar um sensor)\n"
            )

            if choice == "1":
                from app.client import Client

                print("Criando Cliente")
                name = input("Digite o nome (vazio para gerar aleatorio)\n")

                if name == "":
                    name = None

                cliente = Client(name=name)
                from app.client_interface import start

                start(cliente)

            elif choice == "2":
                from app.sensor import Sensor

                print("Criando Sensor")
                name = input("Digite o nome (vazio para gerar aleatorio)\n")
                topic = input("Digite o tópico (vazio para gerar aleatorio)\n")
                monitor = input(
                    "Escolha o parâmetro (digite o número) \n"
                    "1 - Temperatura\n"
                    "2 - Umidade\n"
                    "3 - Velocidade\n"
                    "(vazio para gerar aleatorio)\n"
                )

                if name == "":
                    name = None
                if topic == "":
                    topic = None
                if monitor == "" or monitor.isdigit():
                    monitor = None

                sensor = Sensor(name=name, topic_name=topic, monitor=monitor)
                from app.sensor_interface import start

                start(sensor)

            else:
                print("Opção invalida")

        except Pyro4.errors.CommunicationError as eee:
            from app.server import start_server

            print(eee)

            print("Iniciando servidor")
            start_server()
