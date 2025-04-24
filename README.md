# Yolol Simulator

A Discord bot that simulates the legendary Yolol by responding to messages with either AI-generated replies or random quotes.

## Features

- Responds to `!yolol` command with AI or random quotes
- Responds to any message containing "yolol" (case-insensitive)
- Responds when mentioned or replied to
- Uses OpenAI API for intelligent responses (80% of the time)
- Falls back to random quotes (20% of the time)
- Time-restricted proactive messaging
- Message cleanup functionality

## Setup

1. Clone the repository:
```bash
git clone https://github.com/just-ankur-bagchi/yolol-simulator.git
cd yolol-simulator
```

2. Install dependencies:
```bash
pip install discord.py python-dotenv openai
```

3. Create a `.env` file in the root directory with your configuration:
```
DISCORD_TOKEN=your_bot_token_here
DISCORD_SERVER=your_server_name
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the bot:
```bash
python bot.py
```

## Commands

- `!yolol` - Get a response from Yolol
- `!nolol` - Clean up bot messages and commands

## API Integration

The bot uses OpenAI's GPT-3.5-turbo model to generate more natural and context-aware responses. 
This happens 80% of the time, with the other 20% using classic random quotes from the quotes.txt file.

## Contributing

Feel free to contribute by adding more quotes to `quotes.txt` or improving the bot's functionality! 