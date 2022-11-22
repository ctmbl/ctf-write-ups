The [modulus](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation) is not very long, expressed in bits it is 128 bits. 
We can force it and found its prime factors p and q, I used for example [factordb](http://factordb.com/index.php?query=229086394172560289633018630653414555463&use=x&x=1&VP=on&VC=on&EV=on&OD=on&PR=on&FF=on&PRP=on&CF=on&U=on&C=on&perpage=20&format=1) but I also found an implmentation of a fast factorisation algorithm in `python`, see [`primefac`](https://pypi.org/project/primefac/).

Once you have p and q it is easy to decrypt the cipher and get the message.
You can use `python` together with [`pycryptodome`](https://www.pycryptodome.org/src/public_key/rsa), I personaly used an [online decoder](https://asecuritysite.com/encryption/rsa12_2).  
And here you have the flag!
