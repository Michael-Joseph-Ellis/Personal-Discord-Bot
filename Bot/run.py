from dotenv import load_dotenv
from discord.ext import commands 
import discord
import os

# Load the environment variables
load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

# Define bot intents 
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize the bot 
bot = commands.Bot(command_prefix = './', intents = intents, help_command = None)

# Setup command and event handling 
from bot import register
register(bot)

# Run the bot 
bot.run(token)