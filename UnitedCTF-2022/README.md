# UnitedCTF 2022

## About
UnitedCTF is a CTF organized by multiple student hacking clubs and organizations of Montréal, Québec, mainly [JDIS](https://jdis.ca/), [DCI](https://dciets.com/) and [RHUM](https://ctf2022.unitedctf.ca/rhum) (from UdeS, ETS and UdeM).
It is designed to be a beginner-intermediate oriented CTF to introduce new comers of these clubs to the hacking and CTF world.

## Specs
2022 has been the 3rd edition of the CTF (you can find their archives [here](#links)).
It spread on 1 week from September 30th 2022 to October 7th. The long format is probably chosen to let to beginners the time to discover multiple domains and learn.

It's a Jeopardy CTF and the flag format is `^FLAG-.+$`, the challenges are mainly Web, Crypto and Pwn/Reverse oriented, a bit of Forensic but no OSINT and an original Dynamic Malware Analysis category.

## How to deploy remote challenges
First go to the UnitedCTF-2022 [repo](https://github.com/UnitedCTF/UnitedCTF-2022) and `git clone` it.  
Go to the desired challenge folder
```
cd ./UnitedCTF-2022/challenges/<category>/<challenge>
```

Then build and run the image  
*recommended `name:tag` : `<category/chall>:latest`*  
*recommended container `cont-name` : `<chall>`*  
**the port depends on the challenge, check for `EXPOSE <port>` in each Dockerfile**  
```
docker build -t name:tag .
docker run -it --rm -d --name=cont-name -p<port>:<port> name:tag
```

**Done!** Now you can connect to the remote (running locally here) challenge with `nc localhost <port>`

**DO NOT FORGET** to kill the container and remove the docker image when you're finished, multiple images can be pretty heavy.
```
docker ps --all
docker kill <container_name>
docker images
docker image rm <image_id>
```

## Links
**UnitedCTF 2022**: https://ctf2022.unitedctf.ca/  
**Their solutions**: https://github.com/UnitedCTF/UnitedCTF-2022/  
**Discord**: https://discord.gg/wFxFYJwZ  

*Archives:*  
https://ctf2021.unitedctf.ca/  
https://ctf2020.unitedctf.ca/

### Personnal stats
![](/images/UnitedCTF-2022/Category_Breakdown.png)
![](/images/UnitedCTF-2022/Score_over_Time.png)
