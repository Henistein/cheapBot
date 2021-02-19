from web3 import web3
from dotenv import load_dotenv
import re
load_dotenv()

'''
Script for sending cTH from faucet to users
'''

w3 = Web3(Web3.HTTPProvider('https://node.cheapeth.org/rpc'))
assert w3.isConnected() == True
assert w3.eth.chainId == 777	# check if we are on the right chainid

# check if account can be unlocked from private key
# and set it as default so we can use it later
acct = w3.eth.account.from_key(cTH_private_key)
assert acct.address != None

w3.eth.defaultAccount = acct

p_tokens = [i for i in os.getenv('PARTYTOKENS').split(',')]
p_toke_usage = "{" + os.getenv('PARTYTOKENS') + "}"

# web3
free_cTH_value = os.getenv('FREE_CTH_VALUE')
cTH_private_key = os.getenv('CTH_PRIVATE_KEY')

used_addresses = set([])
used_accountnames = set([])

def extract_address(message):
		p = re.compile('(0x[a-fA-F0-9]{40})')
		result = p.search(message)
		if result == None:
				return None

		return result.group(1)

def send_cth(address):
		# TODO: check why we always get
		# ValueError: {'code': -32000, 'message': 'unknown account'}
		w3.sendTransaction(
				{
						'to': '%s' % address,
						'from': '%s' % w3.eth.defaultAccount.address,
						'value': free_cTH_value
				}
		)


def check_spam(address, author_id):
		spammed = True if address in used_addresses or author_id in used_accountnames else False

		# adding the sender to the mem list
		# quick and dirty according to geraldhost#0182	"Store in memory like true shitcoder"
    # TODO: Don't use memory to store used address and acct ids, BAD IDEA LOL
    # Simple solution would be to use a text file, maybe a serialization format for easier parsing
		used_addresses.add(address)
		used_accountnames.add(author_id)

		return spammed

async def run(message):
		if message.content.split(' ')[1] in p_tokens:
				address = extract_address(message.content)

				# not adding a address is a no go
				if address == None:
						await message.channel.send("Wrong format! Please use `%s [address]` %s" % (p_toke_usage, message.author.mention))
						return

				# users who spam addresses do not get money!
				# addresses which get spammed wont get money!
				spammed = check_spam(address, message.author.id)

				if spammed == True:
						# remove send message and tell not to spam!
						await message.delete()
						await message.channel.send("DON'T SPAM! You already got your free cheapeath! %s" % message.author.mention)
						return

				# send money to the account and notify admins
				send_cth(address)
				await message.channel.send('Ok we will take a look at your request! Its just a matter of time ;) %s' % message.author.mention)
