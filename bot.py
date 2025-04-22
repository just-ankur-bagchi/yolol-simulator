import os
import discord
from discord.ext import commands, tasks
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

# List of user IDs to mention
USERS_TO_TAG = [
    221785345962803200,
    216880230462128131,
    202251384236670977
]

def get_quotes_from_file():
    # read lines is bad if you have too many lines, may need change
    with open('quotes.txt') as f:
        quotes = f.readlines()
        return quotes

def get_proactive_messages():
    with open('proactive.txt') as f:
        messages = f.readlines()
        return messages

async def send_proactive_message():
    # Get a random user to mention
    user_id = random.choice(USERS_TO_TAG)
    # Get a random proactive message
    messages = get_proactive_messages()
    message = random.choice(messages).strip()
    
    # Find the server
    server = discord.utils.get(bot.guilds, name=SERVER)
    if server:
        # Format the message with the user mention
        formatted_message = f"<@{user_id}> {message}"
        # Send to a random channel in the server
        channel = random.choice(server.text_channels)
        await channel.send(formatted_message)

@tasks.loop(minutes=1)
async def check_for_proactive_message():
    # 1/500 chance to send a message
    if random.randint(1, 500) == 1:
        await send_proactive_message()

@bot.event
async def on_ready():
    # initialization
    server = discord.utils.get(bot.guilds, name=SERVER)
    print(f'{bot.user} has connected to Discord!')
    print(f'{server.name}(id: {server.id})')
    # Start the background task
    check_for_proactive_message.start()


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
