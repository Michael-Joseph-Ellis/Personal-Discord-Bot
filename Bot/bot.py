from dotenv import load_dotenv
from discord.ext import commands, tasks
from PIL import Image, ImageOps
import discord
import random
import os 
import io
import aiohttp
import glob 
import markovify

""" # For per-channel Markov chains, we can store the Markov model for each channel in a separate file.
def append_to_file(channel_id, message):
    with open(f"Bot/Text/markov_{channel_id}.txt", "a", encoding="utf-8") as file:
        file.write(message + " ")

def read_from_file(channel_id):
    try:
        with open(f"Bot/Text/markov_{channel_id}.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""
"""
                
def append_to_file(message):
    try:
        with open(f"Bot/Text/markov_shared.txt", "a", encoding="utf-8") as file:
            file.write(message + "\n")  # Add a newline character after each message
    except Exception as e:
        print(f"Failed to write to file: {e}")  # Print the error if writing fails

def read_from_file():
    try:
        with open(f"Bot/Text/markov_shared.txt", "r", encoding="utf-8") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return ""
    except Exception as e:
        return ""

# Dictionary to store message counts for each channel
message_counts_markov = {}
message_counts_gif = {}

# Load the environment variables
load_dotenv()

async def mirror_image(image_bytes):
    # Flips the image horizontally.
    # Load the image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    # Convert image to RGB (in case it's in a different mode)
    image = image.convert("RGB")
    # Mirror the image (flip horizontally)
    mirrored_image = ImageOps.mirror(image)
    # Save the mirrored image to a bytes object
    with io.BytesIO() as image_binary:
        mirrored_image.save(image_binary, format='PNG')
        image_binary.seek(0)  # Go to the start of the bytes object
        return image_binary.read()

async def update_markov_model(message):
    append_to_file(message.content)

    # Increment the Markov-specific message count for the channel
    message_counts_markov[message.channel.id] = message_counts_markov.get(message.channel.id, 0) + 1

    # Trigger Markov generation every 15 messages
    if message_counts_markov[message.channel.id] >= 45:
        message_counts_markov[message.channel.id] = 0  # Reset the Markov message count

        # Read text from file
        text_data = read_from_file()
        word_count = len(text_data.split())

        if word_count > 50:  # Ensure enough data to generate
            model = markovify.Text(text_data, state_size=1)

            sentence = model.make_sentence(tries = 100)

            if sentence:
                await message.channel.send(sentence)
            else:
                await message.channel.send("Not enough unique data to generate a message.")
        else:
            await message.channel.send("Not enough unique data to generate a message.")

# Function to send a random GIF
async def send_random_gif(channel):
    # Selecting a random category of gifs (Frogs or Cats)
    category = random.choice(['Cat', 'Frog'])
    path = f'Bot/GIFs/{category}/*.gif'
    gif_list = glob.glob(path)
    if gif_list:
        gif_path = random.choice(gif_list)
        # Send a GIF
        await channel.send(file=discord.File(gif_path))
    else:
        await channel.send(f"No GIFs found for category: {category}")
    
                
def register(bot):
    
    @bot.event
    # Print the bot's username and ID when it connects to Discord
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')
        change_activity.start() 
        sync_avatar.start()

    @tasks.loop(minutes=10)
    # Change the bot's activity every 10 minutes
    async def change_activity():
        try:
            with open('Bot/Text/activities.txt', 'r') as f:
                activities = f.readlines()
            # Remove whitespace and choose a random activity
            activity = random.choice([line.strip() for line in activities if line.strip()])
            # Set a new presence
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=activity))
            print(f"Changed activity to: {activity}")
        except Exception as e:
            print(f"Error changing activity: {e}")
        
    @tasks.loop(hours=1)
    async def sync_avatar():
        # Synchronize and mirror the bot's avatar with the owner's avatar every hour.
        try:
            user_id = os.getenv('OWNER_USER_ID')  # Make sure this is set in the .env file
            user = await bot.fetch_user(user_id)  # Fetch the user object of the owner

            if user.avatar:
                avatar_url = user.avatar.url

                # Fetch the avatar image
                async with aiohttp.ClientSession() as session:
                    async with session.get(avatar_url) as response:
                        avatar_bytes = await response.read()

                # Mirror (flip horizontally) the avatar
                mirrored_avatar_bytes = await mirror_image(avatar_bytes)

                # Set the bot's avatar to the mirrored version
                await bot.user.edit(avatar=mirrored_avatar_bytes)
                print("Bot's avatar updated to the mirrored version of the owner's avatar.")
            else:
                print("No avatar found for the user.")

        except discord.HTTPException as e:
            print(f"Failed to update avatar due to an HTTP error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
            
        # Function to handle the message event and track counters
        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return

            # Ignore any message that starts with the command prefix (e.g., './')
            if message.content.startswith(bot.command_prefix):
                await bot.process_commands(message)
                return  # Don't add this message to the Markov chain file
            
            # Check if the bot is mentioned and 'thoughts' is in the message 
            if bot.user.mentioned_in(message) and 'thoughts' in message.content.lower():
                try:
                    # Read responses from the dedicated file 
                    with open('Bot/Text/thoughts_responses.txt', 'r') as file:
                        responses = file.readlines()
                        
                    response = random.choice(responses).strip()
                    await message.reply(response)
                except Exception as e:
                    await message.channel.send(f"Error: {str(e)}")  # Send an error message if reading fails
                return  # Avoid triggering other actions if 'thoughts' is mentioned                    

            # Check if the bot is mentioned
            elif bot.user in message.mentions:
                # Send a random response when mentioned
                action = random.choice(['greet', 'gif', 'sentence'])
                if action == 'greet':
                    await message.channel.send("hi!")
                elif action == 'gif':
                    await send_random_gif(message.channel)
                elif action == 'sentence':
                    # Generate and send a Markov sentence if there's enough data
                    text_data = read_from_file()
                    word_count = len(text_data.split())
                    if word_count > 50:
                        model = markovify.Text(text_data)
                        sentence = model.make_sentence(tries=100)
                        if sentence:
                            await message.reply(sentence)
                        else:
                            await message.reply("Not enough unique data to generate a message.")
                    else:
                        await message.reply("Not enough unique data to generate a message.")
                return  # Avoid triggering other actions if mentioned

            # Increment the GIF-specific message count for the channel
            message_counts_gif[message.channel.id] = message_counts_gif.get(message.channel.id, 0) + 1

            # Trigger GIF sending every 10 messages
            if message_counts_gif[message.channel.id] >= 35:
                message_counts_gif[message.channel.id] = 0  # Reset the GIF message count
                await send_random_gif(message.channel)

            # Process the message to update the Markov model
            await update_markov_model(message)

            # Ensure the bot processes any command (e.g., ./help)
            await bot.process_commands(message)
    
    from Commands import bot_help # Import the help command from the help module
    bot_help(bot)
    
    from Commands import bot_changelog # Import the changelog command from the changelog module
    bot_changelog(bot)
    
    from Commands import bot_invite_link # Import the invite command from the invite module 
    bot_invite_link(bot)
    
    from Commands import bot_modif_roles # Import the roles command from the roles module
    bot_modif_roles(bot)
    
    from Commands import bot_leaderboard # Import the leaderboard command from the leaderboard module 
    bot_leaderboard(bot)
    
    from Commands import bot_coinflip # Import the coinflip command from the coinflip module
    bot_coinflip(bot)
    
    from Commands import bot_stalk # Import the stalk command from the stalk module
    bot_stalk(bot)