import os
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

# Create intents object
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # Enable member-related events

bot = commands.Bot(command_prefix='!', intents=intents)


def get_quotes_from_file():
    # read lines is bad if you have too many lines, may need change
    with open('quotes.txt') as f:
        quotes = f.readlines()
        return quotes


@bot.event
async def on_ready():
    # initialization
    server = discord.utils.get(bot.guilds, name=SERVER)
    print(f'{bot.user} has connected to Discord!')
    print(f'{server.name}(id: {server.id})')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel_send(f'very nice {member.name} dude')


@bot.command(name='yolol', help='Chat with Yolol! -- almost the real thing')
async def reply(context):
    bot_quotes = get_quotes_from_file()
    res = random.choice(bot_quotes)
    await context.send(res)


@bot.command(name='g', help='Just fucking g')
async def reply(context):
    await context.send('JUST FUCKING G COOKIES')


@bot.command(name='nolol', help="I don\'t want any more Yolol in my life")
async def clear(context):
    await context.channel.purge(limit=100, check=lambda g: ('!nolol' in g.content) or ('!yolol' in g.content) or (g.author.name == bot.user.name))


@bot.event
async def on_error(event, *args, **kwargs):
    # log messages in a file locally if exceptions occur
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Error during messaging: {args[0]}\n')
        else:
            raise


@bot.event
async def on_message(message):
    # Don't respond to the bot's own messages
    if message.author == bot.user:
        return

    # Check if message contains 'yolol' (case insensitive)
    if 'yolol' in message.content.lower():
        bot_quotes = get_quotes_from_file()
        res = random.choice(bot_quotes)
        await message.channel.send(res)

    # Process commands after checking for 'yolol'
    await bot.process_commands(message)


bot.run(TOKEN)
