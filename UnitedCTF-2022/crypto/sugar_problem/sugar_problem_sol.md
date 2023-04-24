### EN
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

### FR
Le message est en Morse, on le décode avec [CyberChef](https://cyberchef.org/) et on se retrouve avec une chaîne de caractère sans aucun sens.

C'est parce qu'il est aussi chiffré avec une code Vigenere. Pour brute force les code Vigenere j'utilise toujours [dcode](https://www.dcode.fr/chiffre-vigenere) qui est très bien fait. 

On connait une partie du message déchiffré: `FLAG-`

On lance le brute force et on trouve le flag:  
*flag encodé en base64:* `RkxBRy1DSEFNQUxPNExJRkU/Cg==`
