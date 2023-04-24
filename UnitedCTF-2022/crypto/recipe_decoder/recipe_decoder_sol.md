### FR :warning:

Ce challenge a encodé consécutivemnt la même chaîne de caractère.
Les lignes de la recette de cuisine sont encodés chacune avec un de 
ces encodages, donc la déchiffrer c'est déchiffrer le message.

On utilise [CyberChef](https://cyberchef.org/) pour déchiffrer le 
message avec dans l'ordre: 
From Base64 (se reconnaît au padding de `=` à la fin et aux 
caractères présents)
Url Decode (se reconnaît aux %)
From Hex (se reconnaît aux caractères, beaucoup dans le range 
0x30-0x70 c'est de l'ASCII printable)
From decimal (là c'est évident y a que du 0-9, attention à bien
sélectionner le séparateur Colon sur CyberChef)
From charcode (utiliser From Hex fonctionne aussi)

Si vous n'avez pas d'idée, CyberChef a la fonction `Magic` qui va 
essayer plein d'encodages différents (vous pouvez même set une 
profondeur) pour vous aider à trouver !

*flag encodé en base64:* `RkxBRy1TUE9ORy1FTkNPREUK`
