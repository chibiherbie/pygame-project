import socket
import pickle


class Network:
    def __init__(self, password=''):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.163"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

        if password:
            self.client.send(pickle.dumps(password))
            next = self.get_server()
            if next == 'no':
                print('НЕ правильный пароль или нет такого лобби')
                quit()
        else:
            self.client.send(pickle.dumps('new'))
            next = self.get_server()

        self.p, self.open = self.get_server()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass

    def get_server(self):
        try:
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        """
        :return p_x, p_y, bool(pygame.K_f)
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*2))
        except Exception as e:
            print(e)
