# cheapBot - CheapEth Discord Bot

This bot automates a lot of stuff on the cheapETH discord server - WIP

Is cheapEth the future? Hell yeah!

## Usage

**List of commands:**

- [gimme](#gimme)
- [twitter](#twitter)
- [party](#party)
- [clear](#clear)

### <a name="gimme">gimme</a>
Sending the message `$cheap gimme YOUR_CTH_WALLET_ADDRESS_HERE` will make the
bot send a request to a faucet to send you a small amount of cTH (if your are
eligible). 

### <a name="twitter">twitter</a>
Tweet must include one of these: "cheapeth", "cheapethereum", "#cth", "$CTH"
Then post in bot channel, syntax: `$cheap twitter <twitterID> <your cth arrd>`
Get your twitter ID from this site: https://tweeterid.com/
<1000 folllowers = 1cth
1000-2000 followers=2cth
2000+followers=3cth

### <a name="party">party</a>
Call $cheap party to throw a party! no cTH being given, only partyness!

### <a name="speculator">speculator</a>
Speculator detector, not a command, it lurks in the selected channels and waits for speculator.
When it detects one, it throws something at it. Ment to hodl off speculators and show them #speculation.

### <a name = "clear">clear</a>
To clear messages if they contain wallet addresses. By default, `$cheap clear` checks for the last 10 messages in the channel.  
To check for custom nu,ber of messages, say 1000 `$cheap clear 1000`  
Note: Checks for 1000 messages in history starting from latest. Does not mean 1000 removed messages

### <a name="delwalletaddr">delwalletaddr</a>
When channels are passed to `allowed_del_wallet_addr_channels` in *config.py* file, it deletes any further messages with 
wallet addresses in these channels and sends a custom message to the user in DM that the message has been deleted

## Deployment

Before deploying paste your token in config.py
First, install dependencies by calling `pip3 install -r requirements.txt`
Then, simply run the bot by calling `python3 -u -m cheapBot.bot`

## Contributing

In the future this bot will be able to do all sorts of things cheapETH related. If you want to add a command etc take a look at [CONTRIBUTING.md](./CONTRIBUTING.md) we would be happy if you help us grow this bot! The best way to get in touch with us is to join our [Discord server](https://discord.gg/r3WUGxzUH8).

## More info

Wanna to join cheapEth discord? Here is the link: https://discord.gg/r3WUGxzUH8

More infos about cheapEth can be found here: https://cheapeth.org/

## List of contributers

If you think our work is worth some cTH? Why not make us whales? You can find our address below

- Diego: 0x4B49a455fcAe37975d0800C9C415a572FB09f3e1
- Shr1ftyy: 0x3f4e8A8012ccc8E26Be83db3B6d97310271EE001
- henistein: 0xDf1B72FC1bA5a77DD6c038DC2bc70746fFCA5caA
- pasmat: 0x2d10651BC6BC4d18A44100F0C03E3AD02b4f37b8 
- Delta: 0x574E0f8B36A2c40cA664562C334f61B4c6f67Fd6
