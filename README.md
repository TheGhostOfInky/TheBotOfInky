## What is TheBotOfInky?
TheBotOfInky is a bot I devised with the main purpose of doing specific tasks that most common discord bots don't come equipped to handle.

## So what can this bot do?
- Mass purge messages containing certain keywords.
- Clean every message authored by a specific user in a server (even works in users who are no longer in the server).
- Filter words with an unmatched precision.
- Delete specific messages by replying to them.
- Purge all unverified members in a server.
- Purge all deleted accounts from your banlist.
- Prevent specific users of being given specific roles.
- Sussify images (thanks to LinesGuy's [code](https://github.com/LinesGuy/img_sussifier/))

## Requirements:
 - Python 3 (Latest is recommended but any version newer than 3.7 should work fine)
 - discord.py (2.0.0-alpha is needed if you want the bot to support threads, otherwise latest stable, 1.7.3, works fine)
 - python-dotenv (for loading the token from the `.env` file)
 - unidecode (for filter, not needed if you comment out its cog in the `main.py` file)
 - Pillow and Numpy (for image sussifier, not needed if you comment out its cog in the `main.py` file)
 - A discord bot token setup with intents acess

## How to run:
 - Download the repository
 - Rename `sample.env` to `.env` and open it in a text editor (notepad works fine), and replace the "00000.00000.00000" placeholder with your actual discord token and save.
 - Open a terminal/command prompt window in that folder (shift+right click > open command prompt/powershell window here on windows)
 - Type `py main.py` 
 - If everything is setup right you will get the message `YourBotName#1234 has connected to discord`
 - Your bot should now be running, to stop it type ctrl+c in the terminal window or close it.

## Customization
 - To change the command prefix edit the symbol between quote marks in the 7th line of `main.py`
 - To change the words filtered by the auto-filter edit the 4th line of the `filter.py` file, the filter follows the standard [Python regex syntax](https://docs.python.org/3/library/re.html)
 - To change the words cleaned by the clean commands edit the 4th line of the `deleters.py` file, this filter once more follows the standard [Python regex syntax](https://docs.python.org/3/library/re.html)
