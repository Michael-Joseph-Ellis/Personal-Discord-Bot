from discord.ext import commands
import discord

"""
Define bot commands for displaying various leaderboards and leaderboard-related information.

Parameters:
- bot: The Discord bot instance.

Usage:
- `./lb`: Displays an embed with all available leaderboard commands.
- `./lblist`: Shows a list of all leaderboards (placeholder).
- `./tttlb`: Displays the tic-tac-toe leaderboard (placeholder).
- `./fishlb`: Shows the fishing leaderboard (placeholder).
- `./rpslb`: Presents the rock-paper-scissors leaderboard (placeholder).

Preconditions:
- The bot instance must be initialized and connected to the Discord server.
- The bot instance must have all leaderboard commands defined.
- The bot must have permissions to send messages and embeds in the channel.

Returns:
- `./lb`: An embed message containing information about all available leaderboard commands.
- Other commands: Placeholder messages indicating the specific leaderboard (to be implemented).

Raises:
- No specific exceptions are caught or raised in these functions. However, potential Discord API errors may occur if the bot lacks necessary permissions.

Note:
- The main `./lb` command uses a Discord embed to present information in an organized manner.
- The embed for `./lb` is orange-colored and contains fields for each available leaderboard command.
- Other leaderboard commands (`./lblist`, `./tttlb`, `./fishlb`, `./rpslb`) are currently placeholders and send simple text messages.
- These placeholder commands can be expanded in the future to display actual leaderboard data.
- The function demonstrates the use of Discord embeds for creating an informative command response.
- The modular structure allows for easy addition of new leaderboard types in the future.
"""

def bot_leaderboard(bot):
    # Define the leaderboard command 
    @bot.command()
    async def lb(ctx):
        # Define multiple embed pages 
        embeds = [
            discord.Embed(title="Leaderboard Commands", description="Leaderboard commands.", color=discord.Color.orange()),
        ]
        
        embeds[0].add_field(name="./lb", value="Show leaderboard commands.", inline=True)
        embeds[0].add_field(name="./lblist", value="Show all leaderboard.", inline=True)
        embeds[0].add_field(name="./tttlb", value="Show tic-tac-toe leaderboard.", inline=True)
        embeds[0].add_field(name="./fishlb", value="Show fishing leaderboard.", inline=True)
        embeds[0].add_field(name="./rpslb", value="Show rock-paper-scissors leaderboard.", inline=True)
        
        await ctx.send(embed=embeds[0])
        
    @bot.command()
    async def lblist(ctx):
        # Placeholder for leaderboard list 
        await ctx.send("Leaderboard list.")
        
    @bot.command()
    async def tttlb(ctx):
        # Placeholder for tic-tac-toe leaderboard
        await ctx.send("Tic-tac-toe leaderboard.")
    
    @bot.command()
    async def fishlb(ctx):
        # Placeholder for fishing leaderboard
        await ctx.send("Fishing leaderboard.")
        
    @bot.command()
    async def rpslb(ctx):
        # Placeholder for rock-paper-scissors leaderboard
        await ctx.send("Rock-paper-scissors leaderboard.")