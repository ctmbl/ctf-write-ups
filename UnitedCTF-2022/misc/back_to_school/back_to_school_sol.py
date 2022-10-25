"""
Back to school is a simple challenge where you are asked to solve 100 equations 
in less than 3s, of course with a script. 
The equations are linear of 1st order in x: `A*x + B = res`.

Here is my solution: 
"""

from pwn import *

proc = remote("nc.ctf.unitedctf.ca", 5000)
i = 0
while True:
    # If the 100 equations are solved simply print the FLAG:
    if i == 100:
        print(proc.recv().strip().decode())
    print(proc.recvuntil(b": ").strip().decode()) # "Solve : "
    print("\nCalcul:")
    # Gather the equation:
    calcul = proc.recvline().strip().decode() # "4*x - 8 = 24"
    print(calcul)
    print(proc.recvuntil(b": ").strip().decode()) # "Result : "
    eq = calcul.split(" = ") # Split to separate left and right side
    res = int(eq[1]) # res is on the right side
    terms = eq[0].split(" ") # Split left side on 3 diff terms: A, sign, B
    b = int(terms[1]+terms[2]) # b is sign+B
    a = int(terms[0].split("*x")[0]) # a is the first term without the "*x"
    print(f"a={a}; b={b}; res={res}")
    ans = (res-b)/a # Solve eq
    print("Answer = ", ans)
    proc.sendline(bytes(str(int(ans)),"utf-8"))
    #proc.interactive()
    i += 1

