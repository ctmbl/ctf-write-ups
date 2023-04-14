from base64 import b64decode, b64encode
from pwn import *

proc = remote("nc.ctf.unitedctf.ca",3000)

pad = b"A"*10
D = "0123456789abcdef\r"

def brute_force(real, pad, get_bloc):
    i = 0
    guessed = b""
    while i < len(D) and real != guessed:
        #print(i, pad, D[i])
        user = pad + D[i].encode()
        guessed = get_bloc(user)
        i+=1
    i -= 1
    return D[i] if real == guessed else None

def get_token(username):
    print(proc.recvuntil(b"> ").strip().decode())
    proc.sendline(b"2")
    print("Sending: ", username)
    proc.recvuntil(b": ").strip().decode()
    proc.sendline(username)
    proc.recvuntil(b": ").strip().decode()
    token = proc.recvline().strip().decode()
    print("Token is:", token)
    return token

def get_first_bloc(username, size=16):
    token = get_token(username)
    return b64decode(token)[:size]

def get_second_bloc(username, size=16):
    token = get_token(username)
    return b64decode(token)[size:size*2]

def get_third_bloc(username, size=16):
    token = get_token(username)
    return b64decode(token)[size*2:size*3]

def get_fourth_bloc(username, size=16):
    token = get_token(username)
    return b64decode(token)[size*3:size*4]

def get_end(username, size=16):
    token = get_token(username)
    return b64decode(token)[size:]

def flag1():
    pad = b"A"*10
    print("Finding FLAG1")
    flag = b"FLAG-"
    for _ in range(6):
        real = get_first_bloc(pad)
        c = brute_force(real, pad+flag, get_first_bloc)
        flag += c.encode()
        print("FLAG: ", flag)
        pad = pad[1:]
        input()

    print("FLAG has been recovered, let's wrap up the admin token")
    first_bloc = get_first_bloc(b"admin"+flag)
    end = get_end(b"aaaaa")
    token = b64encode(first_bloc+end)
    print("Admin token is:", token)
    proc.interactive()

def flag2():
    pad = b"A"*10
    print("Finding FLAG2")
    flag = b"FLAG-"
    for _ in range(11):
        real = get_first_bloc(pad)
        c = brute_force(real, pad+flag, get_first_bloc)
        flag += c.encode()
        print("FLAG: ", flag)
        pad = pad[1:]
        input()
    pad = b"A"*15
    for _ in range(16):
        real = get_second_bloc(pad)
        c = brute_force(real, pad+flag, get_second_bloc)
        flag += c.encode()
        print("FLAG: ", flag)
        pad = pad[1:]
        input()
    pad = b"A"*15
    for _ in range(16):
        real = get_third_bloc(pad)
        c = brute_force(real, pad+flag, get_third_bloc)
        flag += c.encode()
        print("FLAG: ", flag)
        pad = pad[1:]
        input()
    pad = b"A"*15
    for _ in range(16):
        real = get_fourth_bloc(pad)
        c = brute_force(real, pad+flag, get_fourth_bloc)
        flag += c.encode()
        print("FLAG: ", flag)
        pad = pad[1:]
        input()

flag2()
