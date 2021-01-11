import pickle
import socket
from _thread import *
from game_server import Game
import sys

server = "192.168.0.163"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # тип подключенпия и как передаем информацию

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)  # лимит подключения
print("Waiting for a connection, Server Started")

# players = [Hero('data/image/hero1', 100, 400),
#            Hero('data/image/hero2', 150, 400)]

games = {}


def threaded_client(conn, player, gameId):
    global currentPlayer
    game = games[gameId]

    conn.send(pickle.dumps(game.players[player]))

    reply = (0, 0, 0)

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if gameId in games:
                game = games[gameId]
                game.p_ypd[player] = data
                if not data:
                    print('Disconnected')
                    break
                else:
                    if player == 1:
                        reply = game.p_ypd[0]
                    else:
                        reply = game.p_ypd[1]
                    # print('Recived: ', data)
                    # print('Sendig: ',  reply)
                conn.sendall(pickle.dumps(reply))
        except:
            break

    # try:
    #     del games[gameId]
    #     print("Closing Game", gameId)
    # except:
    #     pass

    print('Lost connection')
    currentPlayer -= 1
    conn.close()


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    currentPlayer += 1
    p = 0
    gameId = (currentPlayer - 1) // 2
    if currentPlayer % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
