from discord.ext import commands 
import discord 
import os 

"""
Define a bot command for displaying changelog information with options to list versions or send detailed changelog files.

Parameters:
- bot: The Discord bot instance.

Usage:
- `./changelog`: Lists all available versions with changelog files.
- `./changelog <version>`: Sends the changelog file for a specific version along with an embed detailing the file content.

Preconditions:
- The bot instance must be initialized and connected to the Discord server.
- The bot instance must have the changelog command defined.
- The bot must have permissions to send messages and embeds in the channel.
- The bot must have read permissions for the changelog directory and files.
- The bot must handle exceptions such as file not found or access errors.

Returns:
- If no version is specified, an embed is sent displaying a list of all available changelog versions.
- If a version is specified, the bot sends an embed with a description and attaches the corresponding changelog file.

Raises:
- FileNotFoundError: If the changelog file for the specified version is not found in the specified directory.
- Exception: If an error occurs while attempting to read or send the changelog file.

Note:
- Changelog files are expected to be stored in the 'Bot/changelog' directory.
- Changelog files should be named in the format 'v<version>.txt', where '<version>' is the version number of the software or bot.
- The function sends an embed with either the list of versions or details of a specific version, improving user interaction by providing direct access to file contents.
"""

def bot_changelog(bot):
    # Define the changelog command
    @bot.command()
    async def changelog(ctx, version: str = None):
        changelog_dir = 'Bot/changelog'  # Set the directory path where changelog files are stored
        if version is None:
            try:
                # List all .txt files and remove the '.txt' extension for display
                versions = [f.replace('.txt', '') for f in os.listdir(changelog_dir) if f.endswith('.txt')]
                versions_list = "\n".join(versions)  # Create a list of versions
            except Exception as e:
                await ctx.send(f"Failed to load versions: {str(e)}")
                return

            embed = discord.Embed(title="Available Versions", description="Specify a version to view details, e.g., `./changelog 1.0.0`", color=discord.Color.blue())
            embed.add_field(name="Versions", value=versions_list, inline=False)
            await ctx.send(embed=embed)
        else:
            filepath = os.path.join(changelog_dir, f'v{version}.txt')  # Construct the filepath for the specific version
            absolute_path = os.path.abspath(filepath)  # Get the absolute path
            try:
                # Check if the file exists
                if not os.path.exists(filepath):
                    raise FileNotFoundError
                # Send the file with an embed
                embed = discord.Embed(title=f"Changelog for Version {version}", description="See the attached file for details.", color=discord.Color.green())
                await ctx.send(embed=embed, file=discord.File(filepath, filename=f"Changelog_v{version}.txt"))
            except FileNotFoundError:
                await ctx.send(f"Changelog for version {version} not found at {absolute_path}. Please make sure the version number is correct.")
            except Exception as e:
                await ctx.send(f"An error occurred at {absolute_path}: {str(e)}")