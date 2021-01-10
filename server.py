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


def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])


def threaded_client(conn, player):
    global currentPlayer
    conn.send(pickle.dumps(players[player]))
    players[player] = ''
    reply = ''
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            players[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                reply = '00,00'
                if player == 1:
                    if type(players[1]) == tuple:
                        reply = players[0]
                else:
                    if type(players[1]) == tuple:
                        reply = players[1]
                print(reply)
                print('Recived: ', data)
                print('Sendig: ',  reply)

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
