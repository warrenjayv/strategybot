import discord
import os
from general import general
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('TOKEN')

genlt = general()


class MyClient(discord.Client):
  
    #~parameters
    storage = []
    counter = 0

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
 
    async def on_message(self, message):
    
        #~store message
        print('Message from {0.author}: {0.content}'.format(message))
        self.storage.append('sniped: `{0.author}`: `{0.content}`'.format(message))
        self.counter += 1
        
        #~reset
        if self.counter > 2:
            self.storage.clear
            self.counter = 0
           
        print("counter: {}".format(self.counter))

        if message.content.startswith('st_ about'):
            await message.channel.send("`strategybot is a turn based, player vs player ancient battle on discord!`")

        if message.content.startswith('st_ snipe'):
            await message.channel.send(self.storage[0])

        if message.content.startswith('st_ attack'):
            # ~ steps ~
            x = 0 

            # ~ set users ~
            mention  = message.mentions[0].display_name
            author   = message.author.name
            genlt.set_user(author , mention)
            genlt.go_defend()
         
            for i in range(12):
                if x < 15:
                    genlt.go_attack(x, 1)
                    x += 1

                land = ' '.join(str(v) for v in genlt.plot)
                if (i < 1):
                    plot = await message.channel.send('{}'.format(land))
                else:
                    await plot.edit(content=land)
                    
                time.sleep(1)

            genlt.clear_users()
            genlt.reset()


client = MyClient()
client.run(TOKEN)