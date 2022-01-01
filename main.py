import discord
import os
from general import general
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('TOKEN')

genlt = general()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content.startswith('st_ about'):
            await message.channel.send("`strategybot is a turn based, player vs player ancient battle on discord!`")

        if message.content.startswith('st_ attack'):
            # ~ set users ~
            mention  = message.mentions[0].display_name
            genlt.set_user(1, mention)

            for i in range(10):
                genlt.go_attack(0, i, 2)
                land = ' '.join(str(v) for v in genlt.plot)
                if (i < 1):
                    plot = await message.channel.send('{}'.format(land))
                else:
                    await plot.edit(content=land)
                    
                time.sleep(2)

            genlt.clear_users()
            genlt.reset()


client = MyClient()
client.run(TOKEN)