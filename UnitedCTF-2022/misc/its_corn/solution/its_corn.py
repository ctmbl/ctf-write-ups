from pwn import remote
import sys, argparse
from time import sleep

from labyrinthe import pathfinding_astar, get_neighboors
print("\n\n/!\ this script uses Daguhh's A* algorithm (https://github.com/Daguhh/Labyrinthe-Astar/)\n\n")

def main():
    # Get the labyrinth and print it
    corn = []
    print("--> Labyrinthe:")
    get_labyrinth(corn)
    for line in corn:
        print(line)

    # Initialize laby parameters
    dim = (len(corn), len(corn[0]))
    S, E = find_S_E(corn)

    # the challenge demands to exclude S and E position
    # so we set up S and E to there closest neighbours that isn't a wall or the map border
    for x,y in neighbours(S,dim):
        if corn[y][x] == ".":
            S = (x,y)
    for x,y in neighbours(E,dim):
        if corn[y][x] == ".":
            E = (x,y)
    print("--> start, end:",S, E)

    # use `labyrinthe.py`'s pathfinding_astar but it returns the positions backwards
    # so invert the list
    path = pathfinding_astar(S, E, corn)[::-1]
    print("--> path:",path)

    print("""!!! The path is in format <x> <y> 
    meaning <column> <row> but
    
    to solve the challenge we need to send it in:
    <row> <column>""")

    print("--> Sending:")
    for i in path:
        msg = bytes(str(i[1]), 'utf-8')+b" "+bytes(str(i[0]), 'utf-8')
        print(msg.decode())
        proc.sendline(msg)
    # when the path is completed we must send a dot
    print(".")
    proc.sendline(b".")

    # Print the flag!
    print(get_line())

def get_line():
    return proc.recvline().strip().decode()

def get_labyrinth(corn):
    """
    Get each lab line and parse it:
    replace whitespaces by dots because `labyrinthe.py` expects dots
    """
    def is_last_line(line):
        """
        It's last labyrinth line if the line is full of # (there is no '.')
        """
        return not "." in line

    # Initialize corn
    corn.append(get_line().replace(" ", "."))
    # Loop until the end (takeing care of the first line)
    while not is_last_line(corn[-1]) or len(corn) == 1:
        corn.append(get_line().replace(" ", "."))

def find_S_E(carte,start="S" ,end="E"):
    """
    Return a tuple of start and end position in a carte
    ((x_start, y_start), (x_end, y_end)) 
    CAUTION: x is column and y row then the corresponding charac is carte[y][x]
    """
    for i in range(len(carte)):
        for j in range(len(carte[0])):
            if carte[i][j] == start:
                S = (j, i)
            if carte[i][j] == end:
                E = (j, i)
    return S,E

def neighbours(node, dim):
    """
    Yield the neighbours position, really just a utility function
    """
    x, y = node
    ROW, COL = dim
    x = x
    y = y
    yield (x, (y+1)%ROW)
    yield (x, y-1)
    yield ((x+1)%COL, y)
    yield (x-1, y)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse args')
    parser.add_argument('host',
                    type=str,
                    help='host of the challenge (localhost?)')
    parser.add_argument('port',
                    type=int,
                    help='Port on which the challenge is running')
    args = parser.parse_args()
    proc = remote(args.host, args.port)

    main()
