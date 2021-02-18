# Party Bot - CheapEth Discord Bot

This bot automates a lot of stuff on the cheapETH discord server - WIP

Is cheapEth the future? Hell yeah!

## Usage

**List of commands:**

- [Party](#party)

### <a name="party">Party</a>

The bot will listen to all messages that start with one of the `PARTYTOKENS`. If the message has the format `[PARTYTOKEN] [ADDRESS]` the bot will store the free cTH request. If someone tries to spam or get money multiple times the spamed messages will be deleted and the users gets an error message.

For example if you want to get your free cTH to the address `0x4B49a455fcAe37975d0800C9C415a572FB09f3e1` you will send the message
`party 0x4B49a455fcAe37975d0800C9C415a572FB09f3e1`

## Deployment

Before deploying create a `.env` file containing the following vars:

```Bash
TOKEN=YOUR_DISCORD_TOKEN
PARTYTOKENS=party,🚀,paaaaaarty

# wallet stuff
CTH_PRIVATE_KEY=YOUR_PRIVATE_KEY
FREE_CTH_VALUE=THE_AMOUNT_SOMEONE_GETS_FREE
```

First, install dependencies by calling `pip3 install -r requirements.txt`
Then, simply run the bot by calling `python3 bot.py`

## Contributing

In the future this bot will be able to do all sorts of things cheapETH related. If you want to add a command etc take a look at [CONTRIBUTING.md](./CONTRIBUTING.md) we would be happy if you help us grow this bot! The best way to get in touch with us is to join our [Discord server](https://discord.gg/r3WUGxzUH8).

## More info

Wanna to join cheapEth discord? Here is the link: https://discord.gg/r3WUGxzUH8

More infos about cheapEth can be found here: https://cheapeth.org/

## List of contributers

If you think our work is worth some cTH? Why not make us a whale? You can find our address below

- Diego: 0x4B49a455fcAe37975d0800C9C415a572FB09f3e1
- Shr1ftyy: 0x3f4e8A8012ccc8E26Be83db3B6d97310271EE001
