import os
import discord
from discord.ext import commands, tasks
import random
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import re
import openai
from prompts import SYSTEM_PROMPT, get_user_prompt

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
OPENAI_API_KEY = os.getenv('openai-key')

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

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

# Global variables for messages
bot_quotes = []
proactive_messages = []

# Regex pattern for matching yolol with any number of 'o's
YOLOL_PATTERN = re.compile(r'yo+l+o+l', re.IGNORECASE)

def load_messages():
    global bot_quotes, proactive_messages
    # Load quotes
    with open('quotes.txt') as f:
        bot_quotes = f.readlines()
    # Load proactive messages
    with open('proactive.txt') as f:
        proactive_messages = f.readlines()

def is_within_active_hours():
    # Get current time in UTC
    utc_now = datetime.now(timezone.utc)
    # Convert to India time (UTC+5:30)
    india_time = utc_now + timedelta(hours=5, minutes=30)
    # Check if time is between 3 PM and 7 PM
    return 15 <= india_time.hour < 19

async def send_proactive_message():
    # Get a random user to mention
    user_id = random.choice(USERS_TO_TAG)
    # Get a random proactive message
    message = random.choice(proactive_messages).strip()
    
    # Find the server
    server = discord.utils.get(bot.guilds, name=SERVER)
    if server:
        # Format the message with the user mention
        formatted_message = f"<@{user_id}> {message}"
        # Send to a random channel in the server
        channel = random.choice(server.text_channels)
        await channel.send(formatted_message)

async def get_ai_response(message_content, referenced_message_content=None):
    """Get a response from OpenAI API based on the message content"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": get_user_prompt(message_content, referenced_message_content)}
            ],
            max_tokens=60,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        # Fallback to random quote
        return random.choice(bot_quotes).strip()

async def send_bot_response(message, referenced_message=None):
    """Send a response, using OpenAI 80% of the time and random quotes 20% of the time"""
    # 80% chance to use OpenAI, 20% chance to use random quotes
    if random.random() < 0.8 and OPENAI_API_KEY:
        referenced_content = None
        if referenced_message:
            referenced_content = referenced_message.content
            
        response = await get_ai_response(message.content, referenced_content)
    else:
        response = random.choice(bot_quotes).strip()
        
    await message.channel.send(response)

@tasks.loop(minutes=1)
async def check_for_proactive_message():
    # Only run between 3 PM and 7 PM India time
    if is_within_active_hours():
        # 1/500 chance to send a message
        if random.randint(1, 100) == 1:
            await send_proactive_message()

@bot.event
async def on_ready():
    # Load messages
    load_messages()
    # initialization
    server = discord.utils.get(bot.guilds, name=SERVER)
    print(f'{bot.user} has connected to Discord!')
    if server:
        print(f'{server.name}(id: {server.id})')
    else:
        print(f'Warning: Could not find server "{SERVER}". Make sure:')
        print('1. The server name in .env matches exactly')
        print('2. The bot has been added to the server')
        print('3. The bot has the necessary permissions')
    # Start the background task
    check_for_proactive_message.start()

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel_send(f'very nice {member.name} dude')

@bot.command(name='yolol', help='Chat with Yolol! -- almost the real thing')
async def reply(context):
    await send_bot_response(context.message)

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

    # Check if message references (replies to) a message from the bot
    is_reply_to_bot = False
    referenced_message = None
    if message.reference and message.reference.message_id:
        # Fetch the message being replied to
        try:
            channel = message.channel
            referenced_message = await channel.fetch_message(message.reference.message_id)
            if referenced_message.author.id == bot.user.id:
                is_reply_to_bot = True
        except discord.errors.NotFound:
            # Message not found, might have been deleted
            pass
        except Exception as e:
            print(f"Error fetching referenced message: {e}")

    # Check if message contains 'yolol' (case insensitive) or if the bot is mentioned
    bot_mentioned = any([
        str(bot.user.id) in message.content,  # Check for raw ID
        f'<@{bot.user.id}>' in message.content,
        f'<@!{bot.user.id}>' in message.content,
        YOLOL_PATTERN.search(message.content) is not None,
        is_reply_to_bot  # Added check for replies to the bot
    ])

    if bot_mentioned:
        await send_bot_response(message, referenced_message)

    # Process commands after checking for mentions
    await bot.process_commands(message)

bot.run(TOKEN)
