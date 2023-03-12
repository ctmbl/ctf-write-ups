## Information
We are given the ip of a machine with the creds of a regular user  
We know that an administrator regularly connects to it  

## Basic Inspection
we can see its home with `ls -lA /home/monkey`  
nothing fancy here, no interesting file and we are not permitted to read or write them  
reading the logs with `cat /var/log/wtmp` we can see its ip and username, (i don't know at all if this step could be interesting or not but here it is)  

## First idea
time has come to know our rights!  
what can we do?
a little `sudo -l` learns us that we have actually great great powers:
```
$ sudo -l

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

[sudo] password for piwie: 
Matching Defaults entries for piwie on 8aabd5f4361e:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User piwie may run the following commands on 8aabd5f4361e:
    (ALL) /usr/bin/strace

```
the `strace` could prove really usefull...

spamming `ps aux` we also see the `monkey` `sshd` process appearing: the admin actually regularly logs in

## Beginning the attack
Let's looks into it:  
with `ps aux` we note:
```
root           1  0.0  0.0  69968  6128 ?        Ss   04:18   0:00 /usr/sbin/sshd -D
```
let's inspect it !

we run `sudo strace -p 1` then wait a bit... we can saw SIGCHILD signal received  
we should follow these processes but the output will be a mess so lets separate it and write it to files:  
`sudo strace -p 1 -ff -o output` should write the output of the diff pid to separate files
here we go !
```
$ sudo strace -p 1 -ff -o output
strace: Process 1 attached
strace: Process 26869 attached
strace: Process 26870 attached
strace: Process 26871 attached
strace: Process 26872 attached
strace: Process 26873 attached
...
```

## Final steps
quite some...
let's look at them, we `cat` the firsts and finally use a grep:
```
cat output.* | grep ZiTF
```
and there we find an interesting info:
```
write(4, "\0\0\0&ZiTF{j9obn4mdn16kp015jkj2kf9"..., 42) = 42
```
This is probably one of the syscalls executed when the admin types its password.

looks promising but we don't have it all so lets write more!  
`sudo strace -p 1 -ff -o output -s 100` should write at most 100 bytes of each string
and there we go:
```
$ cat output.* | grep ZiTF
read(6, "\f\0\0\0&ZiTF{j9obn4mdn16kp015jkj2kf9wlb3z2drc}", 43) = 43
write(4, "\0\0\0&ZiTF{j9obn4mdn16kp015jkj2kf9wlb3z2drc}", 42) = 42
```
flagged!