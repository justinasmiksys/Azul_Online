import socket
import pickle
import tkinter as tk


class Network:

    def __init__(self):
        self.name = ""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.86"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = None
        self.name_request()
        self.connect()

    def name_request(self):

        self.master = tk.Tk()
        self.master.title('Player Name Request')

        tk.Label(self.master, text="Welcome to AZUL!").grid(row=0)
        tk.Label(self.master, text="Please enter your player name.").grid(row=1)
        self.e1 = tk.Entry(self.master)
        self.e1.grid(row=2)

        tk.Button(self.master, text='Confirm', command=self.get_name).grid(
            row=3, sticky='W', pady=4)

        tk.mainloop()

    def get_name(self):
        self.name = self.e1.get()
        self.master.destroy()

    # this is executed first time connecting
    def connect(self):
        try:
            # connects to the server
            self.client.connect(self.addr)
            # receives the id given by the server
            self.id = int(self.client.recv(2048).decode())
            # send the player name to the server
            self.client.send(str.encode(self.name))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*16))

        except socket.error as e:
            print(e)

    def send_data(self, data):
        try:
            self.client.send(str.encode(data))

        except socket.error as e:
            print(e)
