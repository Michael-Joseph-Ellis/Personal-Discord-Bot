from discord.ext import commands
import random
import discord
import asyncio  # To introduce delays

"""
Define a bot command for simulating a coin flip with an animated embed message.

Parameters:
- bot: The Discord bot instance.

Usage:
- `./coinflip`: Initiates a coin flip simulation with an animated embed message.

Preconditions:
- The bot instance must be initialized and connected to the Discord server.
- The bot instance must have the coinflip command defined.
- The bot must have permissions to send messages and embeds in the channel.
- The bot must have permissions to edit its own messages in the channel.

Returns:
- An animated embed message that simulates a coin flip, ending with the final result (Heads or Tails).

Raises:
- No specific exceptions are caught or raised in this function. However, potential Discord API errors may occur if the bot lacks necessary permissions.

Note:
- The function uses asyncio to create delays, simulating the coin flipping process.
- The initial embed is blue, indicating the flip is in progress.
- The final embed is green, indicating the flip has completed.
- The flip animation shows 'Heads' and 'Tails' alternating 15 times before the final result.
- The final outcome is randomly chosen between 'Heads' and 'Tails'.
- The function demonstrates the use of Discord embeds and message editing for creating an interactive command response.
"""

def bot_coinflip(bot):
    # Define the coinflip command
    @bot.command()
    async def coinflip(ctx):
        # Embed for the coin flip process
        embed = discord.Embed(
            title="Coin Flip 🪙",
            description="Flipping the coin...",
            color=discord.Color.blue()
        )

        # Send the initial embed message (before the result)
        message = await ctx.send(embed=embed)

        # Simulate the coin flipping with a delay
        flip_animation = ['Heads', 'Tails'] * 15  # A list to show the coin is flipping

        for i in range(3):  # Show the flip process 3 times
            outcome = random.choice(flip_animation)  # Random temporary outcome
            embed.description = f"Coin flipping... 🪙{outcome}"
            await message.edit(embed=embed)
            await asyncio.sleep(0.1)  # Delay to simulate the flipping process

        # After "flipping", choose the final outcome
        final_outcome = random.choice(['Heads', 'Tails'])

        # Update the embed with the final result
        embed.title = "Coin Flip Result 🪙"
        embed.description = f"The coin landed on: **{final_outcome}**"
        embed.color = discord.Color.green()  # Change color to green to indicate final result
        await message.edit(embed=embed)