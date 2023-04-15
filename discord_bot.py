# bot.py
import os
import discord
from dotenv import load_dotenv
import openai

#mention this new class in commit message
class gptClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
    async def on_message(self, message):
        try:
            messageContent = message.content
            messageArgs = messageContent.split(maxsplit = 3)
            if messageArgs[0] == '!gpt':
                
                match messageArgs[1]:
                    case '--help':
                        r = ("GPTBot is used to answer questions and generate "
                        "images\n\n!gpt [PROMPT]\tPrompt GPTBot with PROMPT arg(-t option to adjust temperature)\n!img [PROMPT]\tPrompt GPTBot"
                        "for image gen with PROMPT arg\n!gpt --help\t  Print out GPTBot commands")
                    case '-t':
                        promptInput = messageArgs[-1]
                        response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=promptInput,
                        max_tokens=1024,
                        temperature=float(messageArgs[2])  
                        )
                        r = response["choices"][0]['text']    
                    case _:
                        
                        promptInput = messageArgs[-1]
                        response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=promptInput,
                        max_tokens=1024,
                        temperature=0.5    
                        )
                        r = response["choices"][0]['text']
                await message.reply(f'```{r}```')
            elif messageArgs[0] == '!img':
                promptInput = messageContent[4:]
                response = openai.Image.create(
                prompt=promptInput,
                n=1,
                size="512x512"
                )
                image_url = response['data'][0]['url']
                await message.reply(image_url)
        except openai.error.InvalidRequestError:
            await message.reply('The prompt you requested in not valid and may have been rejected by our safety system')
        
        except discord.errors.HTTPException:
            await message.reply('The response is to long for discord to display')
            

intents = discord.Intents.default()
intents.message_content = True

client = gptClient(intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
openai.api_key = os.getenv('OPEN_AI_KEY')

client.run(TOKEN)




    

