import discord
from discord.ext import commands
import os
import re

# env
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()

used_addresses = set([])
used_accountnames = set([])


# preprocess the party tokens
p_tokens = [i for i in os.getenv('PARTYTOKENS').split(',')]
p_toke_usage = "{" + os.getenv('PARTYTOKENS') + "}"


def extract_address(message):
    p = re.compile('(0x[a-fA-F0-9]{40})')
    result = p.search(message)
    if result == None:
        return None

    return result.group(1)


def check_spam(address, author):
    spammed = True if address in used_addresses or author in used_accountnames else False

    # adding the sender to the mem list
    # quick and dirty according to geraldhost#0182  "Store in memory like true shitcoder"
    used_addresses.add(address)
    used_accountnames.add(author)

    return spammed


def send_money(address):
    # def need to do smth here
    pass


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.split(' ')[0] in p_tokens:
        address = extract_address(message.content)

        # not adding a address is a no go
        if address == None:
            await message.channel.send("Wrong format! Please use `%s [address]` %s" % (p_toke_usage, message.author.mention))
            return

        # users who spam addresses do not get money!
        # addresses which get spammed wont get money!
        spammed = check_spam(address, message.author.mention)

        if spammed == True:
            # remove send message and tell not to spam!
            await message.delete()
            await message.channel.send("DON'T SPAM! You already got your free cheapeath! %s" % message.author.mention)
            return

        # send money to the account and notify admins
        send_money(address)
        await message.channel.send('Ok we will take a look at your request! Its just a matter of time ;) %s' % message.author.mention)

client.run(os.getenv('TOKEN'))
