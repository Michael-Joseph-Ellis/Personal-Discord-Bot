from discord.ext import commands
import discord
import asyncio

"""
Defines a help command for the bot.

Parameters:
- bot: The discord bot instance.

Usage:
- `./help`: Display a paginated help message with different embed pages for all made commands for the bot.

Preconditions:
- The bot instance must be initialized.
- The bot instance must have the help command defined.
- The bot instance must have the necessary permissions to send messages and add reactions.
- The bot instance must have the necessary permissions to remove reactions.
- The bot instance must have the necessary permissions to clear messages.
- The bot instance must have the necessary permissions to wait for reactions.
- The bot instance must have the necessary permissions to edit messages.

Returns:
- A paginated help message is sent to the channel where the command was called.
- The help message contains different embed pages for all made commands for the bot.
- The user can navigate through the pages using reactions.
- The pagination stops after 60 seconds of inactivity.
- The reactions are removed after the user has reacted.
- The help message is cleared of all reactions after the pagination has stopped.

Raises: 
- Exception: If an error occurs while paginating the help message.

Note:
- The help message is divided into multiple embed pages for different command categories.
- The user can navigate through the pages using reactions.
- The pagination stops after 60 seconds of inactivity.
- The reactions are removed after the user has reacted.
"""

def bot_help(bot):
    # Define the help command
    @bot.command()
    async def help(ctx):
            # Define multiple embed pages
            embeds = [
                discord.Embed(title="General Commands", description="Some general commands.", color=discord.Color.blue()),
                discord.Embed(title="Fun Commands", description="Commands for fun and games.", color=discord.Color.pink()),
                discord.Embed(title="Utility Commands", description="Commands for utility purposes.", color=discord.Color.orange()),
                #discord.Embed(title="Music Commands", description="Commands for music.", color=discord.Color.red()),
                #discord.Embed(title="Moderation Commands", description="Commands for moderation.", color=discord.Color.green())
                # Add more pages as needed
            ]
            
            embeds[0].add_field(name="./help", value="Show this help message.", inline=True)
            embeds[0].add_field(name="./changelog", value="Get bot changelog.", inline=True)
            embeds[0].add_field(name="./invite", value="Get bot invitation.", inline=True)
            
            #embeds[1].add_field(name="./ttt", value="Play tic-tac-toe with another member.", inline=True)
            #embeds[1].add_field(name="./fish", value="Fishing! (WIP)", inline=True)
            #embeds[1].add_field(name="./rps", value="Rock, paper, scissors.. shoo!", inline=True)
            embeds[1].add_field(name="./coinflip", value="Basic coinflip command.", inline=True)
            embeds[1].add_field(name="./stalk", value="See someones activity.", inline=True)
            embeds[1].add_field(name="./lb", value="Show fun activity leaderboard rankings in server.", inline=True)
            
            embeds[2].add_field(name="./roles", value="Show roles commands.", inline=True)
            # You can add more fields to each embed according to your command structure

            # Send the first page
            message = await ctx.send(embed=embeds[0])
            # Add reactions to the message for pagination
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')

            # Define a check function for the reaction
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == message.id

            # Define the index and reaction
            i = 0
            reaction = None

            # Paginate the help message
            while True: 
                if str(reaction) == '➡️' and i < len(embeds) - 1:
                    i += 1
                    await message.edit(embed=embeds[i])
                elif str(reaction) == '⬅️' and i > 0:
                    i -= 1
                    await message.edit(embed=embeds[i])

                # Wait for the next reaction
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                    await message.remove_reaction(reaction, user) # Remove the reaction after the user has reacted
                except asyncio.TimeoutError: # Stop the pagination after 60 seconds
                    break

            await message.clear_reactions()