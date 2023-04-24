#from pwn import xor
from base64 import b64decode

f = open("xorb2_dict.csv","r")
d = f.read().split("\n")
print("Last elt is empty: '", d[-1], "'\nRemoving it")
d=d[:-1]
print("Making my dictionnary bytes")
D = [bytearray(word, "utf-8") for word in d]
print("Done")

b64_flag = b"XWxPUD5HSBhAR1gHVnh9b31mNUg="
xored = b64decode(b64_flag)
flag = bytearray(xored)

# DOESN'T work
def xor(cur, b):
    res = cur.copy()
    for i in range(len(res)):
        res[i] ^= b[i % len(b)]
    return res


print("Dict length:", len(D))
print("Begin xoring")
for w in D:
    flag = xor(flag, w)

print(flag)
