import discord
import re
import os

const port = process.env.PORT || 4000;

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


base_url = "https://twitter.com/"
edited_url = "https://fixupx.com/"
twitter_url_pattern = r'https?://x\.com/([^/]+)/status/(\d+)'

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    matches = re.findall(twitter_url_pattern, message.content)
    
    if matches:
        urls = [f'{match[0]}/status/{match[1].rstrip("/")}' for match in matches]
        embeds_without_description = []
        if message.embeds:
            for embed in message.embeds:
                if re.sub(r'/photo/\d+', '', embed.url[len(base_url):]).rstrip('/') in urls:
                    print(embed.description)
                    if not embed.description:
                        embeds_without_description.append(embed.url)

        if embeds_without_description:
            fixed_urls = [url.replace('https://twitter.com/', 'https://fixupx.com/') for url in embeds_without_description]
            urls_with_borders = '\n'.join([f"||{url}||" for url in fixed_urls])
            await message.reply(f'Fixed the following broken embeds:\n{urls_with_borders}')

# Run the bot with your token
client.run(os.getenv('DISCORD_TOKEN'))
