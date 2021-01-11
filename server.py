import pickle
import socket
from _thread import *
from hero import Hero
import pygame
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

players = [Hero('data/image/hero1', 100, 400),
           Hero('data/image/hero2', 150, 400)]

revel = [(False, '', 1), (False, '', 1)]


def read_pos(d):
    d = d.split(',')
    return d[0], d[1], d[2]


def make_pos(tup):
    return f'{tup[0]},{tup[1]},{tup[2]}'


def threaded_client(conn, player):
    global currentPlayer
    conn.send(pickle.dumps(players[player]))
    players[player] = '00,00,00,00'
    reply = '00,00,00,00'
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            if data[0] != 'player':
                revel[player] = data
                if player == 1:
                    conn.sendall(str.encode(make_pos(revel[0])))
                else:
                    conn.sendall(str.encode(make_pos(revel[1])))
                continue

            if not data:
                print('Disconnected')
                break
            else:
                players[player] = data
                reply = (0, 0, 0)
                if player == 1:
                    if type(players[1]) == tuple:
                        reply = players[0]
                else:
                    if type(players[1]) == tuple:
                        reply = players[1]
                # print('Recived: ', data)
                # print('Sendig: ',  reply)

            conn.sendall(str.encode(make_pos(reply)))
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
