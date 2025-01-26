import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable the 'message_content' intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.embeds:  # Check if the message has embeds
        print("Message contains embeds!")
        for embed in message.embeds:
            if not embed.description:
                print("Description is blank or None!")
            else:
                print("Description:", embed.description)
            
            # Optional: Print timestamp if it's available
            if embed.timestamp:
                print("Timestamp:", embed.timestamp)
            
    else:
        print("Message does not contain embeds.")
    
    await bot.process_commands(message)

bot.run('MTMzMzA5ODM5MTU5MjUwMTI5MA.GukgNL.kNJZSSFlBcqtp7ISfmON-5EK85Z2npabPTwqcM')
