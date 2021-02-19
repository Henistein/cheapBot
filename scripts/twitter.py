import discord
import pickle
import re
import os
import datetime
import json
from jsonrpcclient import request
import requests

"""
Twitter bot

Read discord messages, send request to smart contract
"""

# insert the allowed channels
allowed_channels = ['free-cheapeth-sold-out']

cooldown_list = []


def allow_message(word, cooldown_list):
    for i in cooldown_list:
        if word in i:
            if datetime.datetime.now() > i[1]:
                cooldown_list.remove(i)
                return True
            else:
                return False
    return True


def extract_address(message):
    p = re.compile('(0x[a-fA-F0-9]{40})')
    result = p.search(message)
    if result is None:
        return None
    return result.group(1)


async def run(client, message):
    if message.author == client.user:
        return

    # Check if the address is on message
    if message.content:
        if message.channel.name in allowed_channels:

            if len(message.content.split(' ')) < 4:
                await message.channel.send(
                    "Wrong format %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            # check that 3rd is eth addr
            address = extract_address(message.content)

            # not adding a address is a no go
            if address is None:
                await message.channel.send(
                    "Wrong format %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            user = message.content.split(' ')[2]

            url = 'http://157.245.4.45:5000/send-cth?user=' + str(user) + '&address=' + address
            r = requests.get(url)

            success = r.status_code == 200
            if not success:
                await message.channel.send(
                    "Invalid input %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            # send money to the account and notify admins
            if 'tx' not in r.json():
                await message.channel.send(
                    "Invalid input %s. Use: $cheap twitter <twitterID> <cth address>" % message.author.mention)
                return

            tx_hash = r.json()['tx']

            await message.channel.send(
                'Request sent to contract! %s, userID: %s, tx: %s' % (message.author.mention, user, tx_hash))

            # Cooldown?
