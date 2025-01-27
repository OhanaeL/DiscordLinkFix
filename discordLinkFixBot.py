import discord
from discord.ext import commands
import re
import os
from dotenv import load_dotenv
from flask import Flask
import threading

load_dotenv()

port = int(os.getenv('PORT', 4000))

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

# Flask web server setup
app = Flask(__name__)

# Your base Twitter URL and regex pattern
base_url = "https://twitter.com/"
edited_urls = ["https://fixupx.com/", "https://vxtwitter.com/", "https://fxtwitter.com/"]
blacklist = set()  # Set to keep track of blacklisted users (using their IDs)

twitter_url_pattern = r'https?://x\.com/([^/]+)/status/(\d+)'

# State variables
selected_prefix_index = 0
reply_mode = True  # True: reply, False: send message normally

@app.route('/')
def index():
    print("Heartbeat Pinged!")
    return "Discord Bot is running!"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global selected_prefix_index, reply_mode

    if message.author == client.user:
        return
    
    # Process commands here
    await client.process_commands(message)  # This line allows the bot to process commands


    if message.author.id in blacklist:
        return  # Stop processing the message

    matches = re.findall(twitter_url_pattern, message.content)

    if matches:
        urls = [f'{match[0]}/status/{match[1].rstrip("/")}' for match in matches]
        embeds_without_description = []
        if message.embeds:
            for embed in message.embeds:
                if re.sub(r'/photo/\d+', '', embed.url[len(base_url):]).rstrip('/').split('?')[0] in urls:
                    if not embed.description:
                        embeds_without_description.append(embed.url)

        if embeds_without_description:
            fixed_urls = [
                url.replace(base_url, edited_urls[selected_prefix_index])
                for url in embeds_without_description
            ]
            urls_with_borders = '\n'.join([f"||{url}||" for url in fixed_urls])
            response_message = f'Fixed the following broken embeds:\n{urls_with_borders}'

            if reply_mode:
                await message.reply(response_message)
            else:
                await message.channel.send(response_message)

@client.command(name='prefix')
async def fixPrefixIndex(ctx, arg=None):
    global selected_prefix_index
    try:
        if arg:
            new_index = int(arg)
            if 0 <= new_index < len(edited_urls):
                selected_prefix_index = new_index
                await ctx.send(f"Prefix updated to: {edited_urls[selected_prefix_index]}")
            else:
                await ctx.send("Invalid prefix index. Please choose a valid index.")
        else:
            await ctx.send("Invalid argument. Use 0-2.")
    except Exception as e:
        await ctx.send("An error occurred while processing your request.")
        print(e)

@client.command(name='toggleReply')
async def toggleReply(ctx):
    global reply_mode
    try:
        reply_mode = not reply_mode
        if reply_mode:
            await ctx.send(f"The bot will reply to the messages.")
        else:
            await ctx.send("The bot will no longer reply to the messages.")
    except Exception as e:
        await ctx.send("An error occurred while processing your request.")
        print(e)

@client.command(name='ignoreMe')
async def blackListUser(ctx, arg=None):
    global blacklist
    try:
        user_id = ctx.author.id
        user_nickname = ctx.author.display_name if ctx.author.display_name else ctx.author.name  # Fallback to username if no nickname

        # If the argument is 1, add the user to the blacklist
        if arg == '1':
            blacklist.add(user_id)
            await ctx.send(f"{user_nickname} has been added to the ignore list.")

        # If the argument is 0, remove the user from the blacklist
        elif arg == '0':
            if user_id in blacklist:
                blacklist.remove(user_id)
                await ctx.send(f"{user_nickname} has been removed from the ignore list.")
            else:
                await ctx.send(f"{user_nickname} is not in the ignore list.")
        else:
            await ctx.send("Invalid argument. Use 1 to add to the ignore list and 0 to remove.")
    
    except Exception as e:
        await ctx.send("An error occurred while processing your request.")
        print(e)

# Flask and Discord bot threading
def run_discord_bot():
    client.run(os.getenv('DISCORD_TOKEN'))

def run_flask():
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    run_discord_bot()
