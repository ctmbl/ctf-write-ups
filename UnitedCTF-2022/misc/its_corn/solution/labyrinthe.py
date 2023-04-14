## source: https://github.com/Daguhh/Labyrinthe-Astar/
## adpated by (me): https://github.com/ctmbl/

"""
Implementation of A* pathfinding algorythm  for a small game resolution :
Kirk (represented by a 'T') want to reach the command console ('C'),
activate the command and come back to his starting point.

this script permit to solve this little game and illustrate how those
algorythm work. SHOW_... boolean allow user to activate display of
different numerical treatment that's are performed

for more details :
    import labyrinthe
    help(labyrinthe)

to adjust what you want to be displayed or choose a different map :
have a look to config.py

"""

from itertools import product
import time

global ROW
global COL

DIRECTION = {'DOWN' : (0, 1),
             'UP' : (0, -1),
             'RIGHT' : (1, 0),
             'LEFT' : (-1, 0)}

def pathfinding_astar(start, end, carte):
    """
    A* pathfinding algorythm
    ========================
    Find the shortest path between two nodes

    Algorythm infinite loop :
    -------------------------
    1) ... iterate over all avaible neigbooring squares of {current_node}
    2) ... ... check if the square is an allowed area or go to next one => 1)
    3) ... ... link it to {current_node} as parent
    3) ... ... store it in the {open_dict} to analyse it later on
    4) ... ... test if destination is reached => break the  infinite loop => go to 7)
    5) ... remove node from {open_dict} and store it to {close_dict} so we don't analyse it again
    6) ... choose a new node from {open_dict} with an heuristic function

    7) when done, take the {close_dict} and starting from the end, iterate over parents until come back to start

    Usage : pathfinding_astar(start, end, carte_item) => path

        args:
            start (tuple) : (x, y) starting position
            end (tuple) : (x, y) ending position
            carte_item (function) : return map character at a given position

        return
            path (list) : list of adjacent position == shortest path between start and end nodes
    """
    carte_item = wrap_carte(carte)
    dim = (len(carte), len(carte[0]))
    SHOW_ASTAR = False

    close_dict = {}
    open_dict = {}
    current_node = start

    #init loop
    open_dict[current_node] = {'cost' : 0,
                               'parent' : current_node} #(0, current_node)

    is_reach_end = False
    while not is_reach_end:

        # Display what algorythm do
        if SHOW_ASTAR:
            print_map(current_node, close_dict, open_dict)

        for neighboor_node in get_neighboors(current_node, dim):
            if carte_item(neighboor_node) in ['?', '#']:
                continue

            # test neighbooring node and add it if necessary to open_dict
            open_dict = update_open_dict(current_node, neighboor_node, open_dict, close_dict)

            if end == neighboor_node:
                is_reach_end = True
                close_dict[current_node] = open_dict.pop(current_node)
                close_dict[end] = {'cost' : -1,
                                   'parent' : current_node}
                break
        if is_reach_end == True:
            break

        # don't analyse this node again
        close_dict[current_node] = open_dict.pop(current_node)

        if not open_dict:
            print(f'their is no way from {start} to {end}')
            return None

        current_node = get_next_node(open_dict, end) # heuristic function

    path = get_path(start, end, close_dict)
    return path


def get_neighboors(node, dim):
    """
    A neighboor generator

        args:
            node (tuple) : (x, y) its position

        returns:
            a generator : iterate over top, down, left and right neighboors
    """

    x, y = node
    ROW, COL = dim

    if 0 < y < ROW-1:
        yield (x, y+1)
        yield (x, y-1)

    if 0 < x < COL-1:
        yield (x+1, y)
        yield (x-1, y)


def update_open_dict(parent_node, node, open_dict, close_dict):
    """
    Check if a {node} should be added to the {open_dict} or
    update its parent if the new parent path from start is shorter than the older

        args:
            parent_node (tuple) : position of the node being analysed
            node (tuple) : position of the node to be added in the open_dict
            open_dict (dict) : nodes to be analysed
            close_dict (dict) : nodes already analysed

        returns:
            open_dict (dict): updated version of itself (also changed by side effect, but...)

    """

    new_cost = cost = open_dict[parent_node]['cost'] + 1 # one step further

    # if already analysed
    if node in close_dict.keys():
        return open_dict

    # if not analysed
    if node in open_dict.keys():
        old_cost = open_dict[node]['cost'] # cost of path trought actual parent position
        if old_cost > new_cost:
            open_dict[node] = {'cost' : new_cost, 'parent' : parent_node} # => give it a better parent
        return open_dict

    # else if unknown node
    open_dict[node] = {'cost' : cost, 'parent' : parent_node}
    return open_dict


def get_next_node(open_dict, dest):
    """
    Get the next best node to analyse by computing an heuristic function
    (balance between displacement cost from start and distance from the destination)

        args:
            open_dict (dict) : unanalysed nodes, keys = node position, values = cost and parent
            dest (tuple) : (x, y) currently analysed node position

        return:
            best_node (tuple) : (x, y) position of the next node to analyse
    """

    best_node, best_heuristic = None, 99999

    for node, cost in [(k, v['cost']) for k, v in open_dict.items()]:
        distance = get_distance(dest, node)
        heuristic = cost + distance

        if heuristic < best_heuristic:
            best_node, best_heuristic = node, heuristic

    return best_node


def get_distance(A, B):
    #dist = abs(node[0] - dest[0]) + abs(node[1] - dest[1])*1.1
    #distance = (((node[0] - dest[0])**2 + (node[1] - dest[1])**2)**0.5)*1.25 # false but better looking path
    distance = (
    (
        (
            (B[0] - A[0])**2
          + (B[1] - A[1])**2
        )**0.5
    ) * 1.25
    )
    return distance


def get_path(start_node, dest_node, close_dict):
    """
    Take all analysed node in {close_dict} and by starting from
    {dest}ination node,loop over parent until {start_node} node is reached

        args:
            start_node (tuple) : (x,y) position of starting position
            dest_node (tuple) : (x,y) position of the destination node
            close_dict (dict) : analysed nodes, keys = node position, values = cosst and parent

        returns:
            path (list) : adjacent point froming the shortest path between start and dest_node
    """

    prev_node = dest_node
    path = [prev_node]
    while True:
        prev_node = close_dict[prev_node]['parent']
        path += [prev_node]
        if prev_node == start_node:
            break
    return path


def move(start, path):
    """
    Make character (T) to move and follow the path

        args:
            start (tuple) : (x, y) first position
            path (list) : list of adjacents squares position
    """
    prev_node = start # previous
    for next_node in path:

        if SHOW_MOVE:
            print_map()

        mouvement = (next_node[0]-prev_node[0],
                     next_node[1]-prev_node[1])

        if mouvement == DIRECTION['DOWN']:
            world.move_kirk('DOWN')
        elif mouvement == DIRECTION['UP']:
            world.move_kirk('UP')
        elif mouvement == DIRECTION['RIGHT']:
            world.move_kirk('RIGHT')
        elif mouvement == DIRECTION['LEFT']:
            world.move_kirk('LEFT')

        prev_node = next_node


def pathfinding_brut(start, carte_item, char_researched='?'):
    """
        Brute force version of A* pathfinding algorythm
        Search from a starting postion in the map for a given character

        ARGS:
            start (tuple) : (x, y) starting position
            carte_item (function) : return map character at a given position
            char_researched (str) : infinite loop until it's found

        return
            path (list) : list of adjacent position == shortest path to char_researched
    """

    close_dict = {} # store analysed nodes with postition (tuple) as key
    open_dict = {} # store unanalysed nodes with postition (tuple) as key
    current_node = start # position of node being analysed

    # init loop
    open_dict[current_node] = {'cost' : 0, # displacement cost == number of space to get from start to the square
                               'parent' : current_node} # position of the costless neighboor

    is_dest_reached = False # true if the char_researched in found
    while not is_dest_reached:

        # ENABLE display of what algorythm do
        if SHOW_BRUT:
            print_map(current_node, close_dict, open_dict)

        # look up for possible neigboors and store them
        for neighboor_node in get_neighboors(current_node):
            if not carte_item(neighboor_node) in ['#']:
                open_dict = update_open_dict(current_node, neighboor_node, open_dict, close_dict)

            # stop algorythm
            if carte_item(neighboor_node) == char_researched:
                close_dict[neighboor_node] = open_dict[neighboor_node]
                dest_node = neighboor_node
                is_dest_reached = True
                break

        # nerver look again to the analysed node
        close_dict[current_node] = open_dict.pop(current_node)

        if not open_dict:
            print('There is nothing to do anymore! Bye!')
            return None

        # get the closest (costless) unanalysed node from start position
        current_node = False
        for node, cost in [(k, v['cost']) for k, v in open_dict.items()]:
            for i in range(1000):
                if cost == i:
                    current_node = node
                    break
            if current_node:
                break

    path = get_path(start, dest_node, close_dict)
    return path


def print_map(current_node=(0, 0), close_dict={(0, 0):0}, open_dict={(0, 0):0}):
    """
    Display what algorythms do by representing for each node its state during analysis
        - '*' = analysed
        - '0' = currently analysed
        - 'o' = to be analysed
        - 'T' = "player" actual position
    !!! This function use world instance of World class to keep tracks of the map over iterations !!!

        args:
            current_node (tuple) : currently analysed node
            close_dict (dict) : already analysed nodes
            open_dict (dict) : nodes to ne analysed
    """
    #h, w = len(world.carte), len(world.carte[0])
    #h, w = ROW, COL
    carte_ = [list(row) for row in world.get_carte()]

    for i, j in list(product(range(COL),range(ROW))):

        if (i, j) in close_dict.keys():
            carte_[j][i] = '*'

        if (i, j) in open_dict.keys():
            carte_[j][i] = 'o'

    carte_[current_node[1]][current_node[0]] = '0'
    carte_[kirk.pos[1]][kirk.pos[0]] == 'T'

    print('\n\n')
    for row in carte_:
        print(''.join(row))

    time.sleep(1/SHOW_FRAMERATE)


def print_msg(msg, position='player'):
    """
    Display a message box at player position or in screen center,
    replace character of the map by those of text message

        args:
            msg (list of str) : the message to Display
            position (str) : name of desired placment ('player' or 'center'

    """

    #h, w = len(world.carte), len(world.carte[0])
    carte_ = [list(row) for row in world.get_carte()]

    msg_h = len(msg)
    msg_w = len(msg[0])
    msg_dy = len(msg)
    msg_dx = 2

    if position == 'player':
        kx, ky = kirk.pos
    elif position == 'center':
        kx, ky = int(COL/2-msg_w/2), int(ROW/2+msg_h/2)

    for i, j in list(product(range(msg_w),range(msg_h))):
        carte_[j+ky-msg_dy][i+kx-msg_dx] = msg[j][i]

    print('\n\n')
    for row in carte_:
        print(''.join(row))

    input('')


def wrap_carte(CARTE):
    """
    wrap {CARTE} inbricate list format into a function for easier items access

        args:
            carte (list): a list of lists (rows) of character that represent the map

        returns:
            carte_item (function): f((row, col)) => character (str)
    """

    def carte_item(pos):
        x, y = pos
        return CARTE[y][x]
    return carte_item


###############################################################################


if __name__ == '__main__':
    from world_map import Carte, Kirk
    from messages import find_msg, cant_msg, get_msg, end_msg
    from config import CARTE, SHOW_ASTAR, SHOW_BRUT, SHOW_MOVE, SHOW_FRAMERATE

    ROW = len(CARTE)
    COL = len(CARTE[0])
    kirk = Kirk(CARTE)
    world = Carte(CARTE, kirk)
    start_pos = kirk.pos

    is_fini = False
    while True:

        kr, kc = kirk.pos

        carte=[]
        for row in world.get_carte():
            carte += [row]

        carte_item = wrap_carte(carte)

        start = (kr, kc)

        path = pathfinding_brut(start, carte_item, '?')
        path = path[-1:1:-1]
        move(start, path)

        for j, i  in list(product(range(kc-2, kc+3), range(kr-2, kr+3))): # 5*5 grid around kirk
            if 0 < i < COL and 0 < j < ROW: # and point not out game window
                if carte[j][i] == 'C': # in side of view

                    print_msg(find_msg)
                    path = pathfinding_astar((i,j), start, carte_item) # try to reach it

                    if not path: # path is empty, there is no way to it, can't reach it
                        print_msg(cant_msg)

                    if path != None:

                        # go to 'C' character
                        move(start, path)
                        print_msg(get_msg)

                        # then come back to start point
                        path = pathfinding_astar((i,j), start_pos, carte_item)
                        move(start, path[::-1])
                        print_msg(end_msg, position='center')
                        is_fini = True
                        break
            if is_fini:
                break
        if is_fini:
            break
