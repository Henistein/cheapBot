# Party Bot - CheapEth Discord Bot

Make us whales? 
0x4B49a455fcAe37975d0800C9C415a572FB09f3e1
0x3f4e8A8012ccc8E26Be83db3B6d97310271EE001

This bot automates a lot of stuff on the cheapETH discord server - WIP
Is cheapEth the future? Hell yeah!

## Usage

Before deploying create a `.env` file containing the follwing vars:

```Bash
TOKEN=YOUR_DISCORD_TOKEN
PARTYTOKENS=party,🚀,paaaaaarty

# wallet stuff
CTH_PRIVATE_KEY=YOUR_PRIVATE_KEY
FREE_CTH_VALUE=THE_AMOUNT_SOMEONE_GETS_FREE
```

First, install dependencies by calling `pip3 install -r requirements.txt`
Then, simply run the bot by calling `python3 bot.py`

## Client Usage

The bot will listen to all messages that start with one of the `PARTYTOKENS`. If the message has the format `[PARTYTOKEN] [ADDRESS]` the bot will store the free cTH request. If someone tries to spam or get money multiple times the spamed messages will be deleted and the users gets an error message.

Also, as mentioned above, in the future this bot will be able to do all sorts of things cheapETH related.

## More info

Wanna to join cheapEth discord? Here is the link: https://discord.gg/r3WUGxzUH8

More infos about cheapEth can be found here: https://cheapeth.org/

## Adding more commands
Fork repo, then send a pull request that which meets the following criteria:

 - The script for the command must be placed into the `scripts` folder, with the
	 command suffix as its filename. e.g. calling `$cheap lulz` via discord should
	 call the script `lulz.py` from within the `scripts` folder.

 - The script must have a `run` function, as this is what is called by the
	 `bot.py` script. 


## Structure

![diagram](./imgs/diagram.png)
