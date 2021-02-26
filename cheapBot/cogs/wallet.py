import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from .. import config
from web3 import Web3
from typing import Dict, List

w3 = Web3(Web3.HTTPProvider('https://node.cheapeth.org/rpc'))
deposit_db = TinyDB('db/deposits.json')
query = Query()

class Wallet(commands.Cog):
  bot: commands.Bot
  allowed_channels: List[str]

  def __init__(self, bot: commands.Bot):
    super().__init__()
    self.bot = bot
    self.allowed_channels = config.allowed_game_channels + config.allowed_party_channels
    self.allowed_channels.append('test')

  @commands.command()
  async def createwallet(self, ctx: commands.Context):
    '''
    Creates a new wallet address for the user,
    if he doesn't have one already.
    Deposit your cTH to this address to use in games!
    '''

    if ctx.author.bot:
      return

    if ctx.channel.name in self.allowed_channels:
      message: discord.Message = ctx.message
      uid = str(message.author.id)
      search = deposit_db.search(query.uid == uid)

      # checks if user has a deposit address
      if len(search) == 0:
        acct = w3.eth.account.create()
        deposit_db.insert({'uid': uid, 'dep_addr': acct.address})
        await message.author.send(f':bank: Your deposit address is at: `{acct.address}`\n Private key: {acct.privateKey.hex()} \n PLEASE TAKE NOTE OF IT \n DO NOT SHARE THE PRIVATE KEY WITH ANYONE ELSE')
      else:
        await message.author.send(f'You already have a deposit address at: {search[0]["dep_addr"]}')


  # @commands.command()
  # async def depaddress(self, ctx: commands.Context):
  #   '''
  #   prints the user's deposit wallet address 
  #   '''

  @commands.command()
  async def withdraw(self, ctx: commands.Context, addr: str, amount: str, key: str):

    '''
    Withdraw funds from user's deposit to another wallet 
    (e.g. their main wallet)
    send a direct message to the bot with the following syntax:
    $cheap withdraw  <recepient_address> <amount> <private_key>
    '''

    if ctx.author.bot:
      return

    # Checks if the user is sending the command in private
    if ctx.channel.type == discord.ChannelType.private:
      amount = float(amount)
      message: discord.Message = ctx.message
      uid = str(message.author.id)
      search = deposit_db.search(query.uid == uid)
      from_addr = search[0]['dep_addr']
      dep_acct = w3.eth.account.privateKeyToAccount(key)

      # checks if user has entered the correct corresponding private key 
      if from_addr == dep_acct.address: 
        if len(search) == 0:        
          await message.channel.send("You don't have a deposit address, use $cheap createwallet to create one!")
        else:
          print(from_addr)
          print(key)

          dep_bal = float(w3.fromWei(w3.eth.getBalance(from_addr), 'ether'))
          print(amount, dep_bal)
          if dep_bal >= amount:
            print('here')
            tx = {
              'nonce' : int(w3.eth.getTransactionCount(from_addr)), 
              'gasPrice' : w3.eth.gas_price,
              'gas' : 100000,
              'to' : addr,
              'value' : w3.toWei(amount, 'ether'),
              'chainId' : 777
            }

            signed_txn = w3.eth.account.sign_transaction(tx, key)
            print(f"SIGNED TX: {signed_txn}")
            tx_ret = w3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
            print(tx_ret)
            await message.author.send(f'https://explore.cheapswap.io/tx/{tx_ret}')
          else:
            await message.author.send('You are trying to withdraw more than what is in the deposit')

      else:
        await message.author.send("The private key you have entered is incorrect")
