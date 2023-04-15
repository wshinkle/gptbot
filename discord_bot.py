# bot.py
import os
import discord
from dotenv import load_dotenv
import openai


class gptClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
    async def on_message(self, message):
        try:
            if message.content.startswith('!gpt'):
                
                print(message.content)
                
                promptInput = message.content[4:]
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=promptInput,
                max_tokens=64,
                temperature=0.5    
                )
                r = response["choices"][0]['text']
                print("ANSWER: " + r)
                await message.channel.send(r)
            elif message.content.startswith('!img'):
                promptInput = message.content[4:]
                response = openai.Image.create(
                prompt=promptInput,
                n=1,
                size="512x512"
                )
                image_url = response['data'][0]['url']
                await message.channel.send(image_url)
        except openai.error.InvalidRequestError:
            await message.channel.send('The prompt you requested in not valid and may have been rejected by our safety system')
            

intents = discord.Intents.default()
intents.message_content = True

client = gptClient(intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
openai.api_key = os.getenv('OPEN_AI_KEY')

client.run(TOKEN)




    

