import tkinter as tk
from functools import partial

import Pyro4

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
        }
    }

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

    def create_message(self, messages):
        final_txt = ""

        for message in messages:
            final_txt += f"{message}\n"
        return final_txt

    def set_input_text(self):
        input_value = self.input["input"]["input"].get()
        print(input_value)
        self.update_input_test(input_value)

    def update_input_test(self, value):
        self.input["chat"]["input"].delete(1.0, "end")
        self.input["chat"]["input"].insert("end", value)

    def create_input(self):
        # input
        self.input["input"]["input"] = tk.Entry(self.master, width=self.text_width)
        self.input["input"]["input"].grid(row=self.row, column=1, columnspan=3)
        # button
        # self.row+=1
        self.input["input"]["button"] = tk.Button(self.master, text="Enviar", command=self.set_input_text, bd=3)
        self.input["input"]["button"].grid(row=self.row, column=5, columnspan=1)

        # label_test
        self.row+=1
        self.label_test = tk.Label(self.master, textvariable=self.input["input"]["value"])
        self.label_test.config(font=("helvetica", 10))
        self.label_test.grid(row=self.row, column=0, columnspan=3)

    def create_chat(self):
        # label
        self.input["chat"]["label"] = tk.Label(self.master, text=self.input["chat"]["message"])
        self.input["chat"]["label"].config(font=("helvetica", 10))
        self.input["chat"]["label"].grid(row=self.row, column=0, columnspan=3)
        # chat

        self.row+=1
        self.input["chat"]["input"] = tk.Text(self.master, state="disabled", width=self.text_width)
        scrollbar = tk.Scrollbar(self.input["chat"]["input"])
        scrollbar.place(relheight=1, relx=0.974)

        # self.input["chat"]["input"] = tk.Entry(self.master, state="disabled")
        # self.input["chat"]["input"] = tk.Text(self.master,state="disabled")
        self.input["chat"]["input"].grid(row=self.row, column=0, columnspan=3)
        self.row+=1


    def start(self):
        self.create_input()
        self.create_chat()
        self.create_people()
        # do loop here
        while True:
            self.master.update()

    def select_choice(self):
        pass

    def create_people(self):
        choose = []
        col = 1

        for value in ["joao", "jose", "jose maria da silva souza","joao", "jose","joao", "jose","joao", "jose","joao", "jose","joao", "jose","joao", "jose","joao", "jose","joao", "jose","joao", "jose","joao", "jose",]:
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

            if col == 7:
                self.row += 1
                col = 1

            c.grid(row=self.row, column=col, columnspan=1)
            col += 1
