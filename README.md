# Kemono-Update-Checker
A tool to check new updates from your favorite kemono content creators.

## Table of contents
- [Requirements](#requirements)
- [How to use](#how-to-use)
- [Notes](#notes)

## Requirements
- Python 3.10+
- Discord_Webhook (Optional)

## How to use
1. Download the `kemono-checker` source:

    ```console
    user@host:~$ git clone https://github.com/Bakalhau/Kemono-Update-Checker kemono_checker
    user@host:~$ cd kemono_checker
    ```
2. Configure the application:

    ```console
    user@host:kemono_checker$ mv .env.example .env
    user@host:kemono_checker$ nano .env
    ```

    Change the values of the variables in `.env` as needed.
    Read the comments to guide you. Note that `.env` should be in the root
    directory of this repository.
### How get Discord Webhook Url
	![[webhook.gif]]

3. Configure your creators on `creators.csv`:

    ```csv
    name,service,id
    NAME OF CREATOR,TYPE OF SERVICE (Patreon/Fanbox/etc), ID FROM CREATOR (Get on URL ADRESS)
    ```
    ![[kemono.png]]

4. Run it!

    It will only save all the creator's posts to check if there is anything new in the next run
    ```console
    user@host:kemono_checker$ python3 main.py
    ```

    Now, if you run it, and you have something new from the creator, it should show something like this:
    ```console
    user@host:kemono_checker$ python3 main.py
    # New: Food has been great this season, date: 2023-12-22 15:56:21, url: https://kemono.party/patreon/user/58020585/post/95118501
    ```
    If you want to test if it's working, you can delete some posts from the cache, in the folder `logs/nameofcreator_service.csv`:
    ```csv
    title,date,url,image
    ~~[$10 Tier] Pool Party 2B Stickers/Prints!,2023-12-27 22:45:01,https://kemono.party/patreon/user/5626292/post/95370667,https://img.kemono.su/thumbnail/data/95/07/9507c7604637d5489165f864d436e1cd8cc02a4f76de5711179290b847dfa294.png
    Reze from Chainsaw Man 💥✨,2023-12-22 00:48:44,https://kemono.party/patreon/user/5626292/post/95086844,https://img.kemono.su/thumbnail/data/be/e1/bee1712f401ce4cfc8c542bad9af816cc16004daca06a60c70eb052b45749434.png~~
    POOL PARTY JINX STICKERS!,2023-12-20 22:32:58,https://kemono.party/patreon/user/5626292/post/95021951,https://img.kemono.su/thumbnail/data/59/c7/59c712494d62e3ae087e5a964bc30ec71ae197c6bda94c61a4ac6a274d0ab72c.png
    [$10 Tier] Pool Party Jinx Sticker Sale!,2023-12-20 22:32:44,https://kemono.party/patreon/user/5626292/post/95022006,https://img.kemono.su/thumbnail/data/59/c7/59c712494d62e3ae087e5a964bc30ec71ae197c6bda94c61a4ac6a274d0ab72c.png
    ```

    ```console
    user@host:szuru$ python3 main.py
    # New: [$10 Tier] Pool Party 2B Stickers/Prints!,2023-12-27 22:45:01,https://kemono.party/patreon/user/5626292/post/95370667,https://img.kemono.su/thumbnail/data/95/07/9507c7604637d5489165f864d436e1cd8cc02a4f76de5711179290b847dfa294.png
    # New: Reze from Chainsaw Man 💥✨,2023-12-22 00:48:44,https://kemono.party/patreon/user/5626292/post/95086844,https://img.kemono.su/thumbnail/data/be/e1/bee1712f401ce4cfc8c542bad9af816cc16004daca06a60c70eb052b45749434.png
    ```

    On discord:
    ![[embed.png]]

5. Running it continuously

    Like an update checker, you want it to constantly check for something new, so we need it to run from time to time.

    ## On Linux:
    We have some options here in linux:
    - Crontab
    - Anacron
    - Systemd (Recommended)

    As in my tests it is the easiest and most reliable option, I will show you how to do it in **systemd**:

    First we create a `.service` file in `/etc/systemd/system/`:
    ```console
    user@host:kemono_checker$ sudo nano /etc/systemd/system/kemono_checker.service
    ```

    We need to create a service to run the file, there are many ways to do this, but let's do it simply
    ```console
    # GNU nano 7.2           /etc/systemd/system/kemono_checker.service
    [Unit]
    Description=Kemono Party Update Checker

    [Service]
    Type=oneshot
    WorkingDirectory=/home/user/kemonoparty-checker
    ExecStart=/usr/bin/python3 /home/user/kemonoparty-checker/main.py
    ```

    Now we need to create a timer to run the service from time to time, we can do this with:
    ```console
    user@host:kemono_checker$ sudo nano /etc/systemd/system/kemono_checker.timer
    ```

    Here you can choose the time between each execution [**BE CAREFUL** not to set a time shorter than 10 minutes, you might end up being blocked by kemono's anti-DDOS]
    ```console
    # GNU nano 7.2           /etc/systemd/system/kemono_checker.timer
    [Unit]
    Description=Kemono Timer

    [Timer]
    OnUnitActiveSec=1800s
    OnBootSec=1800s

    [Install]
    WantedBy=timers.target
    ```

    Let's enable and start the service:
    ```console
    user@host:kemono_checker$ sudo systemctl enable kemono_checker.timer
    user@host:kemono_checker$ sudo systemctl start kemono_checker.timer
    ```

    Good job! Now everything is configured, and every X minutes the service should run, even if you restart your computer.

    ## On Windows:

    Well, I'm not a Windows user, so I don't know how to do it, but I believe there are several ways. I'm sure you can do it, I trust your potential!
    ![[good_luck.gif]]

## Notes

### It also works for Coomer.party, check out the Coomer branch! 



    





    