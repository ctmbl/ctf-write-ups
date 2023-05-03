## First things first
We start clasically with a pwn challenge by inspecting the binary we've got!
`file pterodactyle`: it's a x64 ELF executable dyn linked and PIE activated
`ldd pterodactyle`: it's only linked to the libc
`checksec --file=pterodactyle`: full protection, but not Canary -−> maybe a stack buffer overflow is possible ?
ofc we can't know for aslr but we'll assume it's on

we launch the program
2 options:
```
1: Log in
0: Exit
```
too few options we can guess it won't be a UAF
let's try to log in,
we get a `Wrong password`
won't be so easy after all

let's try `strings pterodactyle`
here we go there are a few interesting things here!
```
1: Log in
2: Get cookie
3: Logout
0: Exit
...
Login:
Password:
Wrong password!
Do not try to be smart!
Here, get a cookie! Yum Yum! :-)
Bye bye o/
flag.txt
...
decrypt
...
menu
...
USERNAME
...
open@GLIBC_2.2.5
...
PASSWORD
...
```
 1 - we learn that there are in fact 4 options, may be we should log in to get them ?
 2 - one option is 'Get cookie', is this a leak?
 3 - there is `open@GLIBC` and `flag.txt` so the binary probably embeds a code that reads the flag! we aren't looking for a shell then?
 4 - there are 3 fucntions: main, menu and decrypt, surely disassembling menu will show us the 4 options 
 5 - there are USERNAME and PASSWORD hardcoded strings... and a decrypt function --> maybe we can reverse this one and get the username and password?

so after this little inspection it's time for disassembling and decompiling, the main fucntion as more that 800 instruction so we'll use a tool, objdump won't do for this one
We load the binary in a free online session of binary ninja and start looking at the main

it's a switch case but on the return value of `setjump`??
after a quick research `setjmp` and `longjmp` are fucntions used to do some `goto`s but to external places
OK let's not be messed uo by this weird switch case. It took me some time but finally I understood that simply each time we call `longjmp` (with the `env` parameter and a `val` return value) we jump to `setjmp` so to the switch, `val` is then the return value of the "fake call" to `setjmp`.

Now it's just a normal switch case right?
we notice some interesting things though
especially the case 42 prints the flag!
so we want to try it right? but ofc it doesn't work so easily

after a quick look to the `menu` function we get that it returns -1 in case we enter a number that is <=0 or >3 so we can't just do that, but we notice that the int passed as param to menu is in fact the variable thta control the `puts` of the 2nd and 3rd options!

and then we take a look at the decrypt function
it takes a buffer (and modifies it) and its size as parameters
(then in main this decrypted buffer is compared to USERNAME and PASSWORD) and simply do a xor with `0x77` on each bytes, not what we would called a secure way of storing things, but this is not a reverse challenge.
We then get the bytes stored in the binary which USERNAME and PASSWORD and we xor them using CyberChef and we get:
username: admin
password: MySeCr3TP4$$W0rd
once again this is a pwn challenge ahah

we log in and ask for the cookie and it's not printable ASCII looks good!
/!\ Warning however while looking to decompiled code by binary ninja we won't find this code: a decompiler isn't a perfect tool it soemtimes make mistakes and here is one

but in assembly mode we take a look at this code and see that it writes the `env` (you know the struct that stores the state of the code at the first `setjmp`) to stdout we are good we have our leak!

the buffer overflow is even simpler to find, it's kinda blindingly obvious, there are two calls to `read` when we are asked for the username and the password, and they read 0x80 charac, that is enormous! ofc the buffer is smaller and then we take a look at what we are overidding in gdb and this is the env itself!

sending a username or password of ~ 0x80 bytes proves this theory

[i took a really long time understanding whta's coming next, I've tried to bruteforce it is interesting and should be written, as well as the changing byte per byte to know whicch pointer is rip and whihc byte is the one I should modify]

**HERE** is the formidable Stack Overflow answer that allowed me to get all of this:
https://reverseengineering.stackexchange.com/a/29493
https://reverseengineering.stackexchange.com/questions/29486/how-to-reverse-engineer-a-setjmp-longjmp-sequence

so where to start
first we have to understand how is the env built, but this is architecture dependant so this is a mess to find, here is finally the code of `__setjmp` for the x86_64 archh:
https://sourceware.org/git/?p=glibc.git;a=blob;f=sysdeps/x86_64/setjmp.S;h=a60333566b9c4174d3204dc398606f0897fb7d0a;hb=HEAD
whole doc here:
https://sourceware.org/git/?p=glibc.git;a=tree;f=sysdeps

so we understand that this env is composed of 8 adresses which are:
1st (base=0x00) : rbx         (local)
2nd (base=0x08) : rbp mangled (local)
3rd (base=0x10) : r12         (local)
4th (base=0x18) : r13         (local)
5th (base=0x20) : r14         (local)
6th (base=0x28) : r15         (local)
7th (base=0x30) : rsp mangled (local)
8th (base=0x38) : rip mangled (local)

> I first ran gdb with `b *main+28` to stop on the `setjmp` call and understand what it was but because of the mangling (I didn't know it was mangled at the time) I couldn't guess what was the most interesting pointers.
> I discovered it by overwriing the env by sending payload that looked like `padding + modified_cookie` where padding is 0x20 bytes for the username buffer (for password it's 0x40 so sending a short password permit to not overwrite our own payload) 
> and `modified_cookie` is the cookie we got previously but with only 1 ou 8 bytes modified, just to know what it was modfying.
> It allowed me to understand what was the mangled pointers, but not to understand how they were encrypted, I discovered this a few hours later after trying a useless bruteforce but that's a story for another time.

now we want to understand how they are mangled and why? 
It's actually a glibc protection called Pointer Guard : 
https://sourceware.org/glibc/wiki/PointerEncryption

but how to reverse it to know how to modify the cookie?
the glibc mangling code can be found here:
https://sourceware.org/git/?p=glibc.git;a=blob;f=sysdeps/x86_64/setjmp.S;h=a60333566b9c4174d3204dc398606f0897fb7d0a;hb=HEAD

so the mangling consists of:
rol(ptr XOR key, 17 bits)
to invert it we simply have to perform a ror (bitwise rotation right) of 17 bits and then xor with the key
problem is that we don't know the key, also this key is randomly chose at runtime so unique per process

This is a bit of cryptography but nothing difficult in the end
the really interesting thing is that XOR isn't a good cryptographic function
AND we know part the plain pointers!
in fact rbx is not mangled neither are r12, .. r15
and rbx points to the env variables in the stack, which is not far from the address rbp points to
using rbx as a partial known plain text we can then guess the 12-13 first hexa characters of the address! 
(depending where the stack rabdomly starts (due to ASLR))

that's good we only have 3 charcaters unknwn ! but that's still too high because the CTF doesn't allow bruteforce (but this is clearly bruteforceable)
however we're lucky beacue PIE doesn't randoms the whole address of the program!
In fact the start of the sections PIE chooses always finish by 3 0 hexa charac (meaning in can't start at 0x0..1546 it start at 0x0..X000)
this is a known technics to guess what libc is used on remote using the last 3 hexa characters of symbols but in our case we'll use it as a partial known plain text
and that's perfect because it is exactly what was missing for recovering the whole key!!
And just like that we can guess the key used and then demangle properly rip!

a little schema ?

We can recover rip, adds the delta to make it points to the beginning of the section that prints the flag (remember at the beginning when reversing we noticed this weird 42 option in the switch case that prints the flag)
the we re-mangle the new computed rip, modifies the cookie, add the perfect padding and use the overflow we previously detected!
and that works! we get the flag!

PS: I got very lucky because on remote the leak looks like:
```
0x0
0xf810053be297ca87
0x857d64ca110
0x0
0x0
0x0
0xf810053be157ca87
0x16ea2df3e3a9ca87
```
the stack is not leaked! OFC because this piece of code is heavily platform-dependant and the libc is probably not the same that mine  
luckily for me I don't need to guess the whole key, because even if I don't know the real stack adress I don't need it, only the 3 last hexa character must be changed  
then what I took for the stack leak (0x0) will give me the wrong secret key but because I'll change only the last 3 hexa charcacters and directly re-encrypt the address in the payload it will be transparent, tks to X ^ X ^ A = A and the fact that the mangling isn't chaining the bytes but done byte by byte (this is similar to the AES-ECB vulnerability known is cryptography).
A big tks to [GammaRay99](https://github.com/GammaRay99/CTF-WRITEUPS/tree/main/FCSC2023/pwn/pterodactyle) for making me understand a mistake I didn't even saw!

PS: as already discussed, randomly the exploit can fail because of ASLR poorly randomizing the stack start given us only 12 valid hexa character in common between rbx and rbp and the crashing the program with sigsegv, but trying it a few time it will work!
