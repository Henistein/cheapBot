import os
token = os.getenv('TOKEN')

# Memes
allowed_meme_channels = ['cheap-memes']
min_meme_reaction_approval = 10

# Gimme
allowed_gimme_channels = ['free-cheapeth-sold-out']
faucet_url = 'https://cethswap.com/faucet/?user='
rpc_url = "https://node.cheapeth.org/rpc"

# Twitter 
allowed_twitter_channels = ['free-cheapeth-sold-out']

#Binary only
allowed_binary_channels = ['binary-only']

# Party
allowed_party_channels = ['general', 'crowdsale', 'development', 'rewards', 'speculation', 'non-english', 'cheap-memes', 'zombie-town', 'uses-of-cheapeth', 'hiring', 'website', 'marketing']

# Speculator detector
allowed_check_spec_channels = ['general', 'resources', 'feedback', 'crowdsale','cheap-info', 'development', 'mining', 'rewards', 'speculation', 'non-english', 'cheap-memes', 'zombie-town', 'uses-of-cheapeth', 'hiring', 'website', 'marketing']

# Delete wallet address
allowed_del_wallet_addr_channels = ['development', 'rewards', 'resources', 'feedback']

# Clear channel (of wallet addresses)
allowed_clear_channel_channels = ['general', 'development', 'rewards', 'speculation']
