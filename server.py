import pickle
import socket
from _thread import *
from game_server import Game
import sys

server = "192.168.0.163"  # 15 163
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # тип подключенпия и как передаем информацию

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)  # лимит подключений
print("Waiting for a connection, Server Started")

games = {}


def threaded_client(conn, player, gameId):
    global currentPlayer
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

    games[gameId].count_player -= 1
    currentPlayer -= 1

    conn.send(pickle.dumps((0, 0, 0)))
    pickle.loads(conn.recv(2048))

    del games[gameId]
    print("Closing Game", gameId)
    print('Lost connection')

    conn.close()


currentPlayer = 0


while True:
    conn, addr = s.accept()  # подклчюается user
    print("Connected to:", addr[0])

    data = pickle.loads(conn.recv(2048))  # ждём команды, делать игру или подключаться к существующей

    currentPlayer += 1
    gameId = 0

    if data == 'new':
        gameId = len(games.values()) + 1
        games[gameId] = Game(gameId)
        p = 0
        print("Creating a new game...")
    else:
        for i in range(1, len(games.values()) + 1):
            if games[i].code == data:
                gameId = i
                p = 1

    if gameId:  # если прошло всё успешно, отправляем это, иначе сообщаем об ошибке
        conn.send(pickle.dumps('yes'))
        game = games[gameId]
        game.count_player += 1
    else:
        conn.send(pickle.dumps('no'))

    print('Количество лобби:', len(games.values()))

    try:
        conn.send(pickle.dumps((game.players[p], game.code)))  # отправляем код команты и игроков
        start_new_thread(threaded_client, (conn, p, gameId))  # запускаем игру
    except Exception as e:
        print(e)

