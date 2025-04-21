# Yolol Simulator

A Discord bot that simulates the legendary Yolol by responding to messages with random quotes.

## Features

- Responds to `!yolol` command with random quotes
- Responds to any message containing "yolol" (case-insensitive)
- Includes fun commands like `!g` and `!nolol`
- Message cleanup functionality

## Setup

1. Clone the repository:
```bash
git clone https://github.com/just-ankur-bagchi/yolol-simulator.git
cd yolol-simulator
```

2. Install dependencies:
```bash
pip install discord.py python-dotenv
```

3. Create a `.env` file in the root directory with your Discord bot token and server name:
```
DISCORD_TOKEN=your_bot_token_here
DISCORD_SERVER=your_server_name
```

4. Run the bot:
```bash
python bot.py
```

## Commands

- `!yolol` - Get a random Yolol quote
- `!g` - Special G cookies message
- `!nolol` - Clean up bot messages and commands

## Contributing

Feel free to contribute by adding more quotes to `quotes.txt` or improving the bot's functionality! 