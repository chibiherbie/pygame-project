import socket
import pickle
import json


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.163"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except Exception as e:
            print(e)

    # def save(self, sprite):
    #     with open('save_game1.json', 'w') as file:
    #         print('Saving')
    #         # Create a list of the top left positions and the
    #         # image names.
    #         data = [(sprite.rect.topleft)]
    #         json.dump(data, file)
    #     with open('save_game1.json', 'w') as file:
    #         return json.load(file)
