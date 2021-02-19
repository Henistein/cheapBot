import discord
import scripts.client as cb

'''
Verification script, using the power of memes - WIP
'''

allowed_channels = ['cheap-memes']
meme_list = []

global min_approval 
min_approval = 10


def approved_users(meme_list):
  for i in meme_list:
    if i[3] >= min_approval:
      info = f'{i[2]} {i[3]}'
      cb.sendInfo(info)
      print(info)

def update_list(meme_list):
  for i in meme_list:
    i[3] = 0
    for j in i[0].reactions:
      i[3] += j.count
    if datetime.datetime.now() > i[1]:
      meme_list.remove(i)
  return meme_list

def update_json(meme_list):
  temp = []
  with open("approval.json", "w") as outfile:
    for i in meme_list:
      dictionary = {}
      dictionary["uuid"] = i[2]
      dictionary["reactions"] = i[3]
      if i[3] >= min_approval:
        dictionary["approval"] = True
      else:
        dictionary["approval"] = False
      dictionary["expired_time"] = i[1].__str__()

      temp.append(dictionary)
      json_object = json.dumps(temp)
    outfile.write(json_object)


@client.event
async def on_reaction_add(user, reaction):
  update_list(meme_list)
  update_json(meme_list)
  #approved_users(meme_list)

@client.event
async def on_raw_reaction_remove(payload):
  update_list(meme_list)
  update_json(meme_list)
  #approved_users(meme_list)

async def run(message):
  # Check if an attachment is on the message
  if message.content:
    if message.attachments:
      message_words = message.content.split()
      for word in message_words:
        if re.search("^[- a-fA-F0-9]{36}$", word):
          meme_time = (datetime.datetime.now() + datetime.timedelta(minutes=60))
          meme_list.append([message, meme_time, word, 0])

