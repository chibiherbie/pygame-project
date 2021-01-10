import pickle
import socket
from _thread import *
from hero import Hero
from game import wall, death, hero, all_sprites
import sys

server = "192.168.0.163"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # тип подключенпия и как передаем информацию

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)  # лимит подключения
print("Waiting for a connection, Server Started")

players = [Hero('data/image/hero1', 100, 400, wall, death, hero, all_sprites),
           Hero('data/image/hero2', 150, 400, wall, death, hero, all_sprites)]


def threaded_client(conn, player):
    global currentPlayer
    conn.send(pickle.dumps(players[player]))
    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print('Recived: ', data)
                print('Sendig: ',  reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print('Lost connection')
    currentPlayer -= 1
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
