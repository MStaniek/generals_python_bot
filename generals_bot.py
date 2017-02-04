from socketIO_client import SocketIO
import math
import random
playerIndex=None
generals=None
cities = []
map1 = []

def on_connect():
    print('connect')
    user_id = 'my_example_bot_id'
    socketIO.emit("set_username", user_id, "Testbot")
    custom_game_id = 'my_private_game12345';
    socketIO.emit('join_private', custom_game_id, user_id);
    socketIO.emit('set_force_start', custom_game_id, True);
    print('Joined custom game at http://bot.generals.io/games/' + custom_game_id);


def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_game_start(*data):
    print(data)
    global playerIndex
    playerIndex=data[0]['playerIndex']
    replay_url = 'http://bot.generals.io/replays/' +data[0]['replay_id']
    print('Game starting! The replay will be available after the game at ' + replay_url)

def patch(old, diff):
    print("bliiib", old, diff)
    out=[]
    i=0
    while i < len(diff):
        if(diff[i]):
            out+=old[len(out):len(out)+diff[i]]
        i+=1
        if(i<len(diff) and diff[i]):
            out+=diff[i+1:i+1+diff[i]]
            i+=diff[i]
        i+=1
    print(out)
    return out

def on_game_update(*data):
    global cities, map1

    cities = patch(cities, data[0]["cities_diff"])
    map1 = patch(map1, data[0]["map_diff"])

    generals = data[0]["generals"]
    width = map1[0]
    height = map1[1]
    size = width * height
    print(size, len(map1))
    armies = map1[2:size + 1]
    terrain = map1[-size: -1]
    print("armies", armies)
    print("terrain", terrain)
    print("cities", cities)
    while True:
        index = math.floor(random.random() * size)-1
        #print(index, len(terrain))
        #print([(i, x) for i,x in enumerate(terrain[1:]) if x==playerIndex])
        if terrain[index]==playerIndex:
            row=math.floor(index/width)
            col=index%width
            endIndex=index
            rand=random.random()
            if rand < 0.25 and col > 0:
                endIndex-=1
            elif rand < 0.5 and col< width-1:
                endIndex+=1
            elif rand < 0.75 and row< height-1:
                endIndex+=width
            elif(row > 0):
                endIndex-=width
            else:
                continue

            if(endIndex in cities):
                print("continue")
                continue
            socketIO.emit("attack", index, endIndex)
            print("break")
            break

socketIO = SocketIO('http://bot.generals.io')

socketIO.on('connect', on_connect)

socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)
socketIO.on('game_start', on_game_start)
socketIO.on('game_update', on_game_update)
TILE_EMPTY = -1
TILE_MOUNTAIN = -2
TILE_FOG = -3
TILE_FOG_OBSTACLE = -4



socketIO.wait()
print("hello world")
"""
# Listen
socketIO.on('aaa_response', on_aaa_response)
socketIO.emit('aaa')
socketIO.emit('aaa')
socketIO.wait(seconds=1)

# Stop listening
socketIO.off('aaa_response')
socketIO.emit('aaa')
socketIO.wait(seconds=1)

# Listen only once
socketIO.once('aaa_response', on_aaa_response)
socketIO.emit('aaa')  # Activate aaa_response
socketIO.emit('aaa')  # Ignore
socketIO.wait(seconds=1)
"""