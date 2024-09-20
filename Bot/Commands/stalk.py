from discord.ext import commands
import discord
import requests
import datetime

"""
Define a bot command for retrieving and displaying information about a Roblox user, including their current game status.
This is still VERY WIP. 

Parameters:
- bot: The Discord bot instance.

Usage:
- `./stalk {roblox_username}`: Retrieves and displays information about the specified Roblox user.

Preconditions:
- The bot instance must be initialized and connected to the Discord server.
- The bot must have permissions to send messages and embeds in the channel.
- Internet access is required to fetch data from Roblox APIs.

Returns:
- An embed message containing the Roblox user's information, including:
  - Username
  - Account creation date
  - Profile link
  - Current game being played (if any)

Raises:
- No specific exceptions are raised in the command function, but error messages are sent if user data cannot be retrieved.

Helper Functions:
1. get_roblox_user_info(username):
   - Fetches basic user information from Roblox API.
   - Returns user ID, username, and formatted account creation date.

2. get_current_game(user_id):
   - Retrieves the current game the user is playing using Roblox Presence API.
   - Returns the name of the game or "Not currently playing" if not in a game.

Note:
- The function uses multiple Roblox APIs to gather comprehensive user information.
- Error handling is implemented to manage API request failures gracefully.
- The embed message provides a visually appealing and informative display of user data.
- Debug print statements are included for troubleshooting API responses.
- The function demonstrates integration with external APIs and data processing for Discord bot commands.
- Privacy considerations should be taken into account when using this command, as it retrieves public user data.
"""

# Define a helper function to fetch Roblox user data from API
def get_roblox_user_info(username):
    try:
        # Fetch user ID using Roblox's API to get ID from username
        user_info_url = f"https://users.roblox.com/v1/usernames/users"
        response = requests.post(user_info_url, json={"usernames": [username]}).json()
        if 'data' in response and len(response['data']) > 0:
            user_data = response['data'][0]  # First match
            if 'id' in user_data:
                user_id = user_data['id']
                # Fetch detailed user profile to get the account creation date
                profile_url = f"https://users.roblox.com/v1/users/{user_id}"
                profile_response = requests.get(profile_url).json()
                account_creation = profile_response.get('created', 'Not available')
                # Format the account creation date to exclude milliseconds
                formatted_creation = datetime.datetime.strptime(account_creation, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M")
                return user_id, user_data['name'], formatted_creation
        else:
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Roblox API: {e}")
        return None, None, None

def get_current_game(user_id):
    # Fetching current presence details
    presence_url = f"https://presence.roblox.com/v1/presence/users"
    response = requests.post(presence_url, json={"userIds": [user_id]}).json()
    print(f"Debug - Presence Response: {response}")  # Added detailed debugging
    if 'userPresences' in response and len(response['userPresences']) > 0:
        presence_data = response['userPresences'][0]
        print(f"Debug - Presence Data: {presence_data}")  # More detailed debugging
        if presence_data['userPresenceType'] == 2 and presence_data.get('placeId'):
            place_id = presence_data['placeId']
            game_info_url = f"https://games.roblox.com/v1/games?placeId={place_id}"
            game_info_response = requests.get(game_info_url).json()
            print(f"Debug - Game Info Response: {game_info_response}")  # Additional debugging
            if 'data' in game_info_response and len(game_info_response['data']) > 0:
                return game_info_response['data'][0]['name']
    return "Not currently playing"

def bot_stalk(bot): 
    # Define the stalk command
    @bot.command()
    async def stalk(ctx, roblox_user: str):
        user_id, username, account_creation = get_roblox_user_info(roblox_user)
        if not user_id:
            await ctx.send(f"Could not find Roblox user: {roblox_user}")
            return
        current_game = get_current_game(user_id)  # Fetch current game the user is playing
        # Prepare the embed message
        embed = discord.Embed(
            title=f"Stalking Roblox User: {username}",
            description=f"Account created on: {account_creation}\n[Profile Link](https://www.roblox.com/users/{user_id}/profile)\n**Currently Playing**: {current_game}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)