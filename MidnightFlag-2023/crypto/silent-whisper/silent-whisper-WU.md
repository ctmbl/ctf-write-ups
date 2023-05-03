## First idea
I first think that this was a classic AES-ECB exploit where you guess the secret byte per byte by comparing cipher blocks (because of ECB same plain-text block will give same encrypted blocks) like I did in [the ECB challenge of the United-CTF 2022](https://github.com/ctmbl/ctf-write-ups/tree/main/UnitedCTF-2022/crypto/electronic_code_book).  
But it wasn't! because your input is inserted **after** the secret so you can't shift the secret one byte per one byte in a different block in order to guess it.

## Exploit
So I looked for something else and it turns out that the real vuln was in the unpad! I wouldn't have bet on it...  
It assumes that the last byte is effectively the padding, sooo just modify it and it will unpad more or less byte than it should!!!
> Note: however you can't guess to what byte you should change it, because it will be decrypted and you don't know the key ;)

Doing that you should start to see other things that just the garbage, and playing a bit with it you'll be able to leak the flag!

However you want to change only the padding so it is better if the whole last block is only the padding in this case you'd be sure to modify it.  
Then just send increasingly long username to be encrypted and when the cipher length changes you know that the last block is 16 bytes of `\x10` encrypted, modifying this whole block you're sure to modify the padding! You can also just remove it, in a way this is a modification of the last block :)  
In any case, it will be easier to leak the flag this way!

## Conclusion
The vuln was in the unpad function in the option 2, checking that the padding is less than 16 should fix the vuln!
