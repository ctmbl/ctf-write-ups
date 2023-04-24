Because the exponent used is 0x1=1 the RSA encryption then simplifies to:
```
c = m^e (mod n) = m
```

The message = the cipher which isn't encrypted at all...
Just to transform `c` to hexadecimal base (using `python`) then ASCII (using [CyberChef](https://cyberchef.org/)) and you have the flag:  
*based64 flag:* `RkxBRy1odHRwczovL2dpdGh1Yi5jb20vc2FsdHN0YWNrL3NhbHQvY29tbWl0LzVkZDMwNDI3NmJhNTc0NWVjMjFmYzFlNjY4NmEwYjI4ZGEyOWU2ZmMK`
