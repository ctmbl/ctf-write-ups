The message is Morse Code, we can decode it using [CyberChef](https://cyberchef.org/) 
and we end up with... non-sense string.

The message is still encrypted, but because the characters are letters and 
digits we can guess that the encryption is quite simple: substitution, 
Caesar, Vigenere...

I guessed a Vigenere Code and using [dcode](https://www.dcode.fr/chiffre-vigenere) (which is very well made)
I tried to brute-force it, in this case it's easy because we know a part of
the plain message: `FLAG-` (because we're in a CTF)

And just like this we found the flag!  
*based64 flag:* `RkxBRy1DSEFNQUxPNExJRkU/Cg==`
