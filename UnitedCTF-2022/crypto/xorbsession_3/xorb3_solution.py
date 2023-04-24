from base64 import b64encode, b64decode
import binascii
from random import choice


def xor(cur, b):
    res = cur.copy()
    for i in range(len(res)):
        res[i] ^= b[i % len(b)]
    return res


flag = bytearray(b'FLAG-REDACTEDHEXREDACTEDHEXREDACTEDHE')
keys = [0xa93f9c6f,
     0x3032fa89,
     0xc56714be,
     0x031734d4,
     0x649bf77a,
     0x86cf8750,
     0xec4b53c9,
     0x3c83c74a,
     0x3020cd88,
     0x6de08505,
     0xc7c63073,
     0x35205397,
     0x74ff5323,
     0x5d0a23b2,
     0xc3120ca7,
     0xe0b4e70f,
     0xec2775ea,
     0x15e6ef25,
     0x93fb8172,
     0xda3d1099,
     0x70ac81e7,
     0x601dda5a,
     0x4ba6152e,
     0x068c4540,
     0xde28762f,
     0x7e712461,
     0x05c8cc1c,
     0xaf5e5f01,
     0xb718c86e,
     0xa44e5688,
     0x1da6ef8e,
     0x16be54b0,
     0xe6fcf0e5,
     0x32509a73,
     0x812d83c2,
     0x333af163,
     0x451db1bd,
     0x118e688a,
     0x08f05a43,
     0x334bc7de,
     0x1f8ca915,
     0x66ec0cba,
     0x00b6b560,
     0x1ac2b636,
     0x11e500de,
     0x7bf6763e,
     0xc0eee9fe,
     0x9076ce5d,
     0x25b256d2,
     0xb3e835c7,
     0xf85b6823,
     0xc610f2c2,
     0x0b9f2e6a,
     0x2d2fa455,
     0xbf324a9f,
     0xb66ec850,
     0x9634e995,
     0xa7514ca8,
     0xced21bf7,
     0x81205993,
     0x15c76d19,
     0xbbe9e129,
     0x7aeb3d49,
     0xe4b58dc2,
     0x1b62d7e0,
     0x1fca5d88,
     0x73c6641f,
     0x75e332d1,
     0x6d262dcf,
     0x39b66f5b,
     0xd275277f,
     0xa45eafb2,
     0x04ef0ad7,
     0x7b41d942,
     0x9449d114,
     0xce45761d,
     0xfc159adb,
     0x202a1b1d,
     0x04d312b5,
     0x610ad175,
     0x5cfcc191,
     0xb8f44108,
     0x96b80b97,
     0x36774bd6,
     0x8f653774,
     0x6ba8ec6e,
     0xddf01b17,
     0x0dc42e2a,
     0x8092ebde,
     0x2029b4a4,
     0x006875fd,
     0xb1f05cbb,
     0x0b05c77f,
     0x586f63bb,
     0x55f038a9,
     0x674fbe15,
     0x4652dc61,
     0x044e6e0d,
     0x2102a284
] 

def decode_once(i, flag):
    flag = bytearray(b64decode(flag))
    key = keys[i]
    flag = xor(flag, bytearray(key.to_bytes(4, 'big')))
    #print("DEBUG:",flag)
    return flag

def decode2(step, xored):
    flags= []
    for i in range(len(keys)):
        flag = decode_once(i, xored)
        try:
            flag_s = flag.decode('ascii') # prints the puzzle input
            bytearray(b64decode(flag))
            print(f"--> used key: {hex(keys[i])}, indice {i}")
            print(f"--> FLAG step{step} : ",flag_s)
            flags.append(flag)
        except:
            #print(flag) # prints the puzzle input
            pass
    if len(flags) == 1:
        return flags[0]
    else:
        print("--> CHOICE")
        for i in range(len(flags)):
            print(f" - {i} : ", flags[i])
        i = int(input("Which to choose?"))
        return flags[i]

xored = bytearray(b"zyLDjqVFyZiZUfCtk3Lx7NchroudeuO3sH6pqo5BwK7TItyutTr3s75vsZmXb9DwyF7I7p9j+7KYJdbshFf+iYZnz7KrW625t03eqpJB2+/FZ8+PrizNsbB47KqLb8CaymfTraxj+6O/JNKWlnLLsctZqpqzc/fonyfS7oRGq6OGXK6ymmGsnb9SwqyEUdiYxXfDj5pl/7WZQa25zib2rMVmz6yzY83pmU2tiYpRwJrOTM+yn3PJgrVvqbmTVtPtkCPU6qtbqZq7Jqmqj2/ytspe06+fZuOPmECtrpt73JnKZN/rnnPNrL4n+JSEbcvwyiHTsqtF1pOef62Bkn/cgsxk+ZqmcNafsH7oopF7w/TPZ/m3nWbjv71S7K6KR/KdxGX9iJ46zbiyQNmZhGL+i8hh6a6zYPeiuXm1vohEo+yQINeanWDsn59C7OKTf/nsxXfDi5lh2by9U97rlHvb7sVf6q6zY++VmVPRloxG6qzOd6qvmnPJgZgn+Oubb/aIlyDU6qlg3rmwTfSsj0HIi9NZ+bmdLayWuVGpvoxdzO7LX6uqpWPNlLBAyo2TbK+py2bU7qVz/72ffMrjlkbMmpAjz6KfWtnitX7SrYwm1LzXd8OrmV/Vt7F71r6be9z0ynTf761hrLW7XaiDkk3ykMVZ/a6zc/idu0Leo4x8zIjMdO3pqHDv77Z70uqRfPntziCr7p9x/5W7UN6okSb29Mpn+YGxRd29sXii5g==")

if __name__ == '__main__':
    # SOLUTION:
    print("Xored Flag: ", xored)
    for i in range(10):
        xored = bytearray(decode2(i,xored))
    print(xored)
    exit()

    # ENCRYPTION:
    print("Flag: ", flag)
    for _ in range(10):
        key = choice(keys)
        # print(hex(key)) # print keys
        flag = xor(flag, bytearray(key.to_bytes(4, 'big')))
        flag = bytearray(b64encode(flag))
     
    print(flag.decode('ascii')) # prints the puzzle input
