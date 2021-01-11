import pygame
import socket
import json
import _thread

idGetter = input("Please input player id in int>")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 4444))
pygame.init()
win = pygame.display.set_mode((640, 480))

playerid = int(idGetter)
playercount = []
playerInLobby = 1
rectData = []
playercount.append(playerid)
clock = pygame.time.Clock()


def pop_handler():
    while True:
        val = len(playercount)
        if playerInLobby > 0:
            if len(rectData) > val:
                rectData.pop(0)


def handle_online_player(id):
    while True:
        try:
            recv = sock.recv(1024)
            data = recv.decode()
            data = data.split("}")
            x = json.loads(data[0] + "}")
            if x["id"] == id:
                rectData.append(x)
        except BrokenPipeError as bro:
            pass
        except Exception as e:
            print(e)
            pass


def handle_online_player_join(playerInLobby):
    while True:
        try:
            recv = sock.recv(1024)
            data = recv.decode()
            data = data.split("}")
            x = json.loads(data[0] + "}")
            if x["id"] not in playercount:
                playerInLobby += 1
                playercount.append(x["id"])
                print("another player has joined")
                _thread.start_new_thread(handle_online_player, (x["id"],))
        except Exception as e:
            # print(e, data)
            pass


_thread.start_new_thread(handle_online_player_join, (playerInLobby,))
_thread.start_new_thread(pop_handler, ())

pygame.display.set_caption(f"Pygame window {playerid}")

black = (0, 0, 0)
white = (255, 255, 255)

player_width = 40
player_height = 40
player_pos_x = 0
player_pos_y = 0
velocity = 0.3
frameRate = 1

gameActive = True

while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameActive = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_pos_x -= velocity * frameRate
    if keys[pygame.K_RIGHT]:
        player_pos_x += velocity * frameRate
    if keys[pygame.K_UP]:
        player_pos_y -= velocity * frameRate
    if keys[pygame.K_DOWN]:
        player_pos_y += velocity * frameRate

    data = {}
    data['id'] = playerid
    data['x-pos'] = player_pos_x
    data['y-pos'] = player_pos_y
    json_data = json.dumps(data)
    sock.sendall(json_data.encode())
    win.fill(black)
    for rect in rectData:
        pygame.draw.rect(win, (255, 0, 0), (rect["x-pos"], rect["y-pos"], 40, 40))
    pygame.draw.rect(win, white, (player_pos_x, player_pos_y, player_width, player_height))
    pygame.display.update()
