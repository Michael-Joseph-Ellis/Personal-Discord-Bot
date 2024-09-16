from dotenv import load_dotenv
from discord.ext import commands 
import discord
import os

"""
Define a bot command that generates an invitation link for the bot and sends it embedded in a Discord message.

Parameters:
- bot: The Discord bot instance. This must be initialized and running as part of a Discord bot application.

Usage:
- `./invite`: When this command is executed in a Discord channel where the bot has permissions to send messages, it will generate and display an invite link for the bot.

Details:
- The function constructs a URL that directs users to Discord's OAuth2 authorization flow for adding bots. The URL includes the bot's client ID and the permissions integer.
- The invite link is presented within a Discord embed, making it easy for users to see and click to add the bot to their server.
- The bot's client ID and permissions level are hardcoded but can be adjusted as needed for different deployment environments or permission requirements.

Embed Information:
- Title: "Invite me to your server."
- Description: Provides a brief explanation and a prompt to invite the bot.
- Color: The embed uses a blue color for aesthetic purposes.

Optional Fields:
- The embed can be extended with additional fields, such as "Required Permissions," if more detailed information about bot permissions needs to be provided to the user.

Returns:
- The function does not return a value but sends an embedded message to the context from which the command was invoked.

Raises:
- The function itself does not explicitly raise exceptions, but if there are issues with sending messages or constructing the embed, discord.py may raise related exceptions.

Note:
- Ensure that the `client_id` is correctly set to the bot's client ID before using the command.
- Adjust the `permissions` integer based on the actual permissions needed for the bot to function as intended on a server.
"""

def invite_link(bot):
    @bot.command()
    async def invite(ctx):
        # Define the client ID and the permissions integer
        load_dotenv()
        client_id = os.getenv('CLIENT_ID')  # Replace this with your actual bot's client ID
        permissions = os.getenv('PERMISSION_ID')  # Example permissions integer; adjust as necessary
        
        # Create the invite URL
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot"

        # Create an embed for the invite link
        embed = discord.Embed(
            title="Invite me to your server.",
            description="Click the link below to invite me to your server.",
            color=discord.Color.blue()
        )
        
        # Add the invite link as a field in the embed
        embed.add_field(name="Invite Link", value=f"[Click Here to Invite]({invite_url})", inline=False)

        # Optionally, you can add more fields to describe what your bot does or the permissions it requires
        # embed.add_field(name="Required Permissions", value="This bot requires Administrator permissions for full functionality.", inline=False)

        # Send the embed
        await ctx.send(embed=embed)