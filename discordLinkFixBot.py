import discord
import re
import os
from dotenv import load_dotenv
from flask import Flask
import threading
import asyncio

load_dotenv()
# Environment variables and setup
port = int(os.getenv('PORT', 4000))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Flask web server setup
app = Flask(__name__)

# Your base Twitter URL and regex pattern
base_url = "https://twitter.com/"
edited_url = "https://fixupx.com/"
twitter_url_pattern = r'https?://x\.com/([^/]+)/status/(\d+)'

@app.route('/')
def index():
    print("Heartbeat Pinged!")
    return "Discord Bot is running!"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await asyncio.sleep(2)
    
    matches = re.findall(twitter_url_pattern, message.content)
    
    if matches:
        urls = [f'{match[0]}/status/{match[1].rstrip("/")}' for match in matches]
        print(urls)
        embeds_without_description = []
        if message.embeds:
            for embed in message.embeds:
                print(embed.url)
                if re.sub(r'/photo/\d+', '', embed.url[len(base_url):]).rstrip('/').split('?')[0] in urls:
                    print(embed.description)
                    if not embed.description:
                        embeds_without_description.append(embed.url)

        if embeds_without_description:
            fixed_urls = [url.replace('https://twitter.com/', 'https://fixupx.com/') for url in embeds_without_description]
            urls_with_borders = '\n'.join([f"||{url}||" for url in fixed_urls])
            await message.reply(f'Fixed the following broken embeds:\n{urls_with_borders}')

def run_discord_bot():
    client.run(os.getenv('DISCORD_TOKEN'))

def run_flask():
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    run_discord_bot()
