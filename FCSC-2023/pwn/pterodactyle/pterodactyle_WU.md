## Binary file inspection
First things first guys,  
We start as usual with a pwn challenge by inspecting the binary we've got!  
`file pterodactyle`: it's a x64 ELF executable dyn linked and PIE activated  
`ldd pterodactyle`: it's only linked to the libc  
`checksec --file=pterodactyle`: full protection, but not Canary -−> maybe a stack buffer overflow is possible?  
Of course, we can't know if ASLR is ON because it's a platform protection not a binary one, but we'll assume it is!

We launch the program (hoping it's not a malware but let's trust them <3 )  
2 options are presented to us:
```
1: Log in
0: Exit
```
Currently there is too few options, we can guess it won't be a UAF exploit, but it's just a guess!

Let's try to log in with random creds,  
we get a `Wrong password`, it won't be so easy after all :')

Let's try `strings pterodactyle`, we can often learn a lot doing that!  
Here we go, at last we discover a few interesting things!  
(I've shown only the interesting parts)
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
Here is what I concluded reading this:
- we learn that there are in fact 4 options, maybe we must log in to get them?
- one option is 'Get cookie', is this a leak?
- there is `open@GLIBC` and `flag.txt` so the binary probably embeds a code that reads the flag! Maybe we aren't looking for a shell then, but just to jump to that part of the code
- there are 3 fucntions: `main`, `menu` and `decrypt`, surely disassembling menu will show us the 4 options
- there are `USERNAME` and `PASSWORD` symbols... and a `decrypt` function --> could we reverse this one and get the username and password to log in?

## Getting our hands dirty
So after this little inspection it's time for disassembling and decompiling, the main function as more that 800 instructions so we'll use a tool, `objdump` won't do for this one :')


### `main`
We load the binary in a [free online session of binary ninja](https://cloud.binary.ninja/) (but you can choose `ghidra`, `ida`, or `cutter` shouldn't be much of a difference) and start looking at the main.
```
add main code
```
It's a switch case but on the return value of `setjump`?? Wtf is that?

After a quick research `setjmp` and `longjmp` are functions used to do some `goto`s but to external places.  
OK let's not be confused by this weird switch case. It took me some time but finally I understood that each time we call `longjmp` (with the `env` parameter and a `val` return value) we jump to the point where `setjmp` was first called, `val` is then the return value of the "fake call" to `setjmp`.  
Now it's just a normal switch case right?

We notice some interesting things though, especially the case 42 prints the flag, that's awesome!  
So why don't we try it right now? You'll notice also that nothing seems to forbid us to jump to the 2nd and 3rd options that are hidden.  
We'll notice that in menu `longjmp` is called with the return value of menu +1 so to access case 42 we must enter 41, same for the other options.

But of course it doesn't work so well :') : `Do not try to be smart!`

### `menu`
Now let's look at the `menu` function.
```
add menu code
```
After a quick look, we get that it returns -1 in case we enter a number that is <=0 or >3 so we can't just do that, but we notice that the int passed as param to menu is in fact the variable that controls the `puts` of the 2nd and 3rd options! So we guess that logging in will allow us these options.  
But we still have to log in...

### `decrypt`
and then we take a look at the decrypt function
```
add decrypt code
```
It takes a buffer (and modifies it) and its size as parameters and simply do a xor with `0x77` on each bytes, not what we would called a secure way of storing secrets, but this is not a reverse challenge.
> Note: in main this decrypted buffer is compared to USERNAME and PASSWORD!
 
We then get the bytes stored in the binary which are USERNAME and PASSWORD and we xor them using CyberChef and we get:
```
username: admin
password: MySeCr3TP4$$W0rd7
```
once again this is a pwn challenge ahah

## Start exploiting things
### the leak
We log in and ask for the cookie, it's not printable ASCII: looks good!
> /!\ Warning however looking to decompiled code with binary ninja we won't find this code: a decompiler isn't a perfect tool it sometimes makes mistakes that we must detect!

In assembly mode we take a look at this code and see that it writes the `env` (you know the struct that stores the state of the code at the first `setjmp`) to `stdout` we are good we have our leak!  
Let's write a little pwntools script to display it! (properly)
```
...
Here, get a cookie! Yum Yum! :-)
leak: b'\x08\xec\x80"\xfc\x7f\x00\x00o\x8b?j\xbeDT\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x18\xec\x80"\xfc\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x10I\xd0\xf8\x7f\x00\x00o\x8b\x7fl\xbeDT\xb4o\x8b\xe1y|\xceL\xe1'
addresses:
0x7ffc2280ec08
0xb45444be6a3f8b6f
0x0
0x7ffc2280ec18
0x0
0x7ff8d0491020
0xb45444be6c7f8b6f
0xe14cce7c79e18b6f
```
> Note: this is what it looks like in local not in remote, you'll see later that this is important

Looks good, we seems to have some stack addresses and some garbage, don't know what is it at the time, but we'll come to it later!

### the Stack Buffer Overflow
OK we've got our leak but it won't help us printing the flag...  
We must find a way to redirect the execution, meaning overwrite rip somewhere, so let's look for buffer overflows!

Actually the buffer overflow is even simpler to find, it's kinda blindingly obvious.

We noticed previouly when dumping the strings that the `read` symbols was used so we just check that every call do/do not overflow its buffer.  
There are two calls to `read` when we are asked for the username and the password, and they read 0x80 characters, that is enormous!  
Of course, the buffer is smaller:
```
add the asm code
```
Then we take a look at what we are overidding in gdb (`b *main+212`) and this is the env struct itself!

sending a username or password of 0x80 bytes proves this theory:
```
 $ ./pterodactyle 
1: Log in
0: Exit
>> 1
Login:
>> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Password:
>> Wrong password!
Segmentation fault
```
a SIGSEGV, I like that smell!

### the BIG problem
> I took a veryyyyyy long time (like almost 8-10h) understanding what's coming next, I've first tried to bruteforce  

> **HERE** is the formidable Stack Overflow answer that allowed me to get all of this:
https://reverseengineering.stackexchange.com/a/29493

So where do we start?

First, we have to understand how is the env built, but this is architecture dependant so this is a mess to find, here is finally the [code of `__setjmp` for the x86_64 arch](https://sourceware.org/git/?p=glibc.git;a=blob;f=sysdeps/x86_64/setjmp.S;h=a60333566b9c4174d3204dc398606f0897fb7d0a;hb=HEAD) (I keep only the interesting part) (sorry it's in AT&T syntax...):
```
ENTRY (__sigsetjmp)
        /* Save registers.  */
        movq %rbx, (JB_RBX*8)(%rdi)
...
        movq %rbp, (JB_RBP*8)(%rdi)
...
        mov %RBP_LP, %RAX_LP
        PTR_MANGLE (%RAX_LP)
        mov %RAX_LP, (JB_RBP*8)(%rdi)
...
        movq %r12, (JB_R12*8)(%rdi)
        movq %r13, (JB_R13*8)(%rdi)
        movq %r14, (JB_R14*8)(%rdi)
        movq %r15, (JB_R15*8)(%rdi)
        lea 8(%rsp), %RDX_LP
...
        PTR_MANGLE (%RDX_LP)
...
        movq %rdx, (JB_RSP*8)(%rdi)
        mov (%rsp), %RAX_LP     /* Save PC we are returning to now.  */
        LIBC_PROBE (setjmp, 3, LP_SIZE@%RDI_LP, -4@%esi, LP_SIZE@%RAX_LP)
...
        PTR_MANGLE (%RAX_LP)
...
        movq %rax, (JB_PC*8)(%rdi)
```
and here is the [whole doc](https://sourceware.org/git/?p=glibc.git;a=tree;f=sysdeps)

So we understand (really??!) that this env is composed of 8 adresses which are (we don't know the remote arch so we can't know what it is but we'll assume that it is the same):
```
1st (base=0x00) : rbx         (local)
2nd (base=0x08) : rbp mangled (local)
3rd (base=0x10) : r12         (local)
4th (base=0x18) : r13         (local)
5th (base=0x20) : r14         (local)
6th (base=0x28) : r15         (local)
7th (base=0x30) : rsp mangled (local)
8th (base=0x38) : rip mangled (local)
```

> I first ran gdb with `b *main+28` to stop on the `setjmp` call and understand what it was but because of the mangling (I didn't know it was mangled at the time) I couldn't guess what was the most interesting pointers.  
> I discovered it by overwriting the env by sending payload that looked like `padding + modified_cookie` where padding is 0x20 bytes for the username buffer (for password it's 0x40 so sending a short password permit to not overwrite our own payload)  
> and `modified_cookie` is the cookie we got previously but with only 1 ou 8 bytes modified, just to know what it was modfying.  
> It allowed me to understand what was the mangled pointers, but not to understand how they were encrypted, I discovered this a few hours later after trying a useless bruteforce...

### ...and the solution
now we want to understand how they are mangled and why?

It's actually a glibc protection called [Pointer Guard](https://sourceware.org/glibc/wiki/PointerEncryption), I'd already heard about it but never encounter it in a challenge...

But how to reverse it to know how to modify the cookie?

The glibc mangling code for x86_64 can be found [here](https://codebrowser.dev/glibc/glibc/sysdeps/unix/sysv/linux/x86_64/sysdep.h.html#_M/PTR_MANGLE) 

It's basically a XOR with a random-runtime-chosen key (explained at [Pointer Guard glibc wiki](https://sourceware.org/glibc/wiki/PointerEncryption)) and then a bitwise rotation left:  
`rol(<ptr> XOR key, 17 bits)`

So to invert it, we simply have to perform a `ror` (bitwise rotation right) of 17 bits and then a XOR with the key!  
Only one problem: we don't know the key... (and it is randomly chosen at runtime)

However, XOR isn't a good cryptographic function **AND** we know part of the plain pointers!

Ok, let's what information we've got:
 - rbx is not mangled neither are r12, .. r15
 - looking at in gdb **(local)**, rbx points to the env variables in the stack, which is not far from the address rbp points to!
 - then using rbx as a partial known plain text we can then guess the 12-13 first hexa characters of the address! (depending on where the stack rabdomly starts due to ASLR)

That's good we only have 3 charcaters unknown!  
But that's still too high because the CTF doesn't allow bruteforce (but this is clearly bruteforceable)...

However we're lucky because PIE *(Position Independant Executable)* doesn't random the whole address of the program base!
In fact the start of the sections PIE chooses always finish by 3 0 hexa charac  
*Meaning: it can't start at 0x0..1546*   
*it starts at 0x0..Y000*

This is a well known technic to guess what libc is used on remote using the last 3 hexa characters of leaked symbols but in our case we'll use it as a partial known plain text.

And that's perfect because it is exactly what was missing for recovering the whole key!!  
Here is a little schema to understand it (we ignore the bitwise rotation here)
```
we'll use:
rbp_mangled = rbp XOR key 
key = rbp_mangled XOR rbp
key_truncated|garbage = rbp_mangled XOR rbp_truncated|garbage
but remember: rbx is close to rbp so:
rbp_truncated = rbx_truncated 
and we know plain rbx!

LEAKED STACK: 0x 00 00 7f fc 22 80 eX XX (truncated)
RBP MANGLED : 0x b4 54 44 be 6a 3f 8b 6f
PARTIAL KEY :                       X XX 




COMPLETE KEY: 0x d5 8c 98 36 12 e8 a8 1f
```

And just like that we can guess the key used and then demangle properly rip!

We can recover rip, adds the delta to make it points to the beginning of the section that prints the flag (remember at the beginning when reversing we noticed this weird 42 option in the switch case that prints the flag)
the we re-mangle the new computed rip, modifies the cookie, add the perfect padding and use the overflow we previously detected!
and that works! we get the flag!

## Post Scriptums and mea culpa
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

**PPS:** as already discussed, randomly the exploit can fail because of ASLR poorly randomizing the stack start given us only 12 valid hexa character in common between rbx and rbp and the crashing the program with sigsegv, but trying it a few time it will work!
