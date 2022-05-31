import random
import tkinter as tk
from tkinter import ttk

import Pyro4

from app.client import Client
from config import PYRO_URL


class Interface:
    master = tk.Tk()
    # master.geometry('200x150')

    form = {}
    checkbox = {}
    input = {
        "input": {
            "value": tk.StringVar(),
            "message": "Digita algo ai",
            "label": None,
            "button": None,
            "input": None
        },
        "chat": {
            "value": tk.StringVar(),
            "message": "Este é o chat",
            "label": None,
            "button": None,
            "input": None
        },
        "select": {
            "value": tk.StringVar(),
            "message": "Selecione a sala",
            "label": None,
            "button": None,
            "input": None
        },
        "people": {
            "value": tk.StringVar(),
            "message": "Participantes",
            "label": None,
            "button": None,
            "input": None
        },
        "room": {
            "value": tk.StringVar(),
            "message": "Criar sala",
            "label": None,
            "button": None,
            "input": None
        }
    }
    popup = None

    OPTIONS_ROW = 5
    TEXT_COL = 10
    topics = []
    choose = []
    buffer = []
    buffer_len = 50
    broker = Pyro4.core.Proxy(PYRO_URL)
    label_test = None

    row = 0

    text_width=50
    chatrooms = []

    client = None

    def __init__(self, name):
        self.client = Client(name=name)

    def create_message(self, messages):
        final_txt = ""

        for message in messages:
            final_txt += f"{message}\n"
        return final_txt

    def send_message(self):
        input_value = self.input["input"]["input"].get()
        print(f"enviando: {input_value} - {self.get_room()}")
        self.client.send_message(input_value,room=self.get_room())

    def get_room(self):
        return self.input["select"]["value"]

    def update_input_test(self, value):
        self.input["chat"]["input"].delete(1.0, "end")
        self.input["chat"]["input"].insert("end", value)

    def create_input(self):
        # input
        self.input["input"]["input"] = tk.Entry(self.master, width=self.text_width)
        self.input["input"]["input"].grid(row=self.row, column=0, columnspan=3)
        # button
        self.input["input"]["button"] = tk.Button(self.master, text="Enviar", command=self.send_message, bd=3)
        self.input["input"]["button"].grid(row=self.row, column=3, columnspan=1)
        self.row +=1
        # label
        self.input["input"]["label"] = tk.Label(self.master, text="Enviando para")
        self.input["input"]["label"].config(font=("helvetica", 10))
        self.input["input"]["label"].grid(row=self.row, column=0, columnspan=3)
        self.row +=1

    def create_chat(self):
        # label
        self.input["chat"]["label"] = tk.Label(self.master, text=self.input["chat"]["message"])
        self.input["chat"]["label"].config(font=("helvetica", 10))
        self.input["chat"]["label"].grid(row=self.row, column=0, columnspan=3)
        # chat
        self.row+=1
        self.input["chat"]["input"] = tk.Text(self.master, state="normal", width=self.text_width)
        scrollbar = tk.Scrollbar(self.input["chat"]["input"])
        scrollbar.place(relheight=1, relx=0.974)

        self.input["chat"]["input"].grid(row=self.row, column=0, columnspan=3)
        self.row+=1

    def create_dropdown(self):
        # label
        self.input["select"]["label"] = tk.Label(self.master, text=self.input["select"]["message"])
        self.input["select"]["label"].config(font=("helvetica", 10))
        self.input["select"]["label"].grid(row=self.row, column=0, columnspan=1)

        # select
        self.input["select"]["value"].set("nenhuma")
        self.input["select"]["input"] = tk.OptionMenu(self.master, self.input["select"]["value"],"nenhuma", *self.chatrooms)
        self.input["select"]["input"].grid(row=self.row, column=1, columnspan=1)

        # button
        self.input["select"]["button"] = tk.Button(self.master, text="Atualizar lista", command=self.update_chatrooms, bd=3)
        self.input["select"]["button"].grid(row=self.row, column=2, columnspan=1)
        self.row +=1

        self.input["select"]["button"] = tk.Button(self.master, text="popup", command=self.popup_bonus, bd=3)
        self.input["select"]["button"].grid(row=self.row, column=2, columnspan=1)
        self.row +=1


    def update_chatrooms(self):
        self.chatrooms = list(self.client.rooms)

        menu = self.input["select"]["input"]["menu"]
        variable = self.input["select"]["value"]
        menu.delete(0, "end")
        variable.set("nenhuma")

        menu.add_command(label="nenhuma",
                         command=lambda value="nenhuma": variable.set(value))

        for string in self.chatrooms:
            menu.add_command(label=string,
                             command=lambda value=string: variable.set(value))


    def popup_bonus(self):

        if self.popup:
            return

        self.popup = tk.Toplevel()
        self.popup.wm_title("Window")

        self.input["room"]["label"] = tk.Label(self.popup, text=self.input["room"]["message"])
        self.input["room"]["label"].config(font=("helvetica", 10))
        self.input["room"]["label"].grid(row=0, column=0, columnspan=2)

        # input
        self.input["room"]["input"] = tk.Entry(self.popup, width=self.text_width)
        self.input["room"]["input"].grid(row=1, column=0, columnspan=3)

        b = ttk.Button(self.popup, text="Okay", command=self.create_room)
        b.grid(row=2, column=0)

    def create_room(self):
        print(f"criadno nova sala {self.input['room']['input'].get()}")
        room = self.input['room']['input'].get()
        self.client.send_message("Criando nova sala", room)
        self.popup.destroy()
        self.popup = None


    def start(self):
        self.create_input()
        self.create_chat()
        self.create_people()
        self.create_dropdown()
        # do loop here

        while True:
            self.master.update()
            self.client.update()
            self.update_input_test("\n".join(self.client.messages))



    def select_choice(self):
        pass

    def create_people(self):
        self.input["people"]["label"] = tk.Label(self.master, text=self.input["people"]["message"])
        self.input["people"]["label"].config(font=("helvetica", 10))
        self.input["people"]["label"].grid(row=self.row, column=0, columnspan=1)
        self.row +=1

        choose = []
        col = 0

        for value in self.client.get_participants():
            var = tk.BooleanVar()
            choose.append(var)
            c = tk.Checkbutton(
                self.master,
                text=value,
                variable=var,
                onvalue=1,
                offvalue=0,
                command=self.select_choice,
            )

            if col == 3:
                self.row += 1
                col = 0

            c.grid(row=self.row, column=col, columnspan=1)
            col += 1

        self.row +=1