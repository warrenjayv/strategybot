import discord
import os
from general import general
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('TOKEN')

class MyClient(discord.Client):
  
    #~parameters
    storage = []
    counter = 0
    isActive = 0 

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

        if message.content.startswith('st_ about'):
            await message.channel.send("`strategybot is a turn based, player vs player ancient battle on discord!`")

        if message.content.startswith('st_ snipe'):
            await message.channel.send(self.storage[0])

        if message.content.startswith('st_ attack'):

            #~notify
            if self.isActive == 1:
                await message.channel.send("`a battle is ongoing; please try again later. =[`")
                return
 
            self.isActive = 1

            genlt = general()

            # ~ steps ~
            x = 0 
            
            plot = ''
            
            # ~ set users ~
            mention  = message.mentions[0].display_name
            author   = message.author.name
            genlt.set_user(author , mention)
            genlt.go_defend()
         
            while (genlt.health1 > 0) and (genlt.health2 > 0):
                  
                genlt.set_health()
                
                if x < 12:
                    genlt.go_attack(x, 1)

                if x > 12:
                    genlt.do_battle() 

                land = ' '.join(str(v) for v in genlt.plot)
                if (x < 1):
                    plot = await message.channel.send('{}'.format(land))
                else:
                    await plot.edit(content=land)
                    
                time.sleep(1)

                x += 1

            genlt.conclude()
            end = ' '.join(str(v) for v in genlt.plot)
            await plot.edit(content=end)
            genlt.clear_users()
            genlt.reset()
            self.isActive = 0
            

client = MyClient()
client.run(TOKEN)