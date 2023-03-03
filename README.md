## What is TheBotOfInky?
TheBotOfInky is a bot I devised with the main purpose of doing specific tasks that most common discord bots don't come equipped to handle.

## So what can this bot do?
- Purge all deleted accounts from your banlist.
- DM moderators a list of all banned users in a guild.
- DM users Unicode escaped messages.
- Check polcompballvalues backend status and reminds users to upload their scores.
- List all emojis in a given server.
- Echo message to another channel.
- Search specific mediawiki wikis for a given page.
- List roles, show server profile and global banner background.
- Sussify images (thanks to LinesGuy's [code](https://github.com/LinesGuy/img_sussifier/)).

## Requirements:
 - Python 3 (Latest is recommended but any version newer than 3.10 should work fine)
 - The following packages (listed in the requirements.txt file)
    - Nextcord (2.0.0 or newer is needed, 2.4.0+ recommended)
    - python-dotenv (for loading the token from the `.env` file)
    - Pillow, Numpy, python-ffmpeg (for image sussifier, not needed if you comment out its cog in the `main.py` file)
 - FFMPEG installed and added to PATH (for image sussifier, not needed if you comment out its cog in the `main.py` file)
 - A discord bot token setup with intents access

## How to run:
 - Clone the repository.
 - Rename `sample.env` to `.env` and open it in a text editor. Replace the "00000.00000.00000" placeholder with your actual discord token and save.
 - Open a terminal/command prompt window in that folder (shift+right click > open command prompt/powershell window here on windows).
 - Type `py -m pip install -r requirements.txt`(Windows) or `python3 -m pip3 install -r requirements.txt`(POSIX) to download all needed packages (FFMPEG not included).
 - Type `py main.py` (Windows) or `python3 main.py` (POSIX) to tun the bot.
 - If everything is setup right you will get the message `YourBotName#1234 has connected to discord`.
 - Your bot should now be running, to stop it type ctrl+c in the terminal window or close it.

## Customization
 - To change the command prefix add a `DISCORD_PREFIX` key to the `.env` file

## Warnings
 - `battery` command only works inside of termux environments with the termux api installed and correctly setup.
 - If you are running the bot on a big endian CPU, you might need to change the color format on the ffmpeg stream from `bgr32` to `rgb32`, open a new issue if you get corrupt images when running this command.