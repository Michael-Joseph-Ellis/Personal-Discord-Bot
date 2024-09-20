from discord.ext import commands 
import discord 
import asyncio 

"""
Define bot commands for managing and displaying roles within a Discord server.

Parameters:
- bot: The Discord bot instance.

Usage:
- `./roles`: Displays an embed with all available role management commands.
- `./roleslist`: Shows a paginated list of all roles in the server.
- `./setrole {@user} {role_name}`: Assigns a role to a user.
- `./removerole {@user} {role_name}`: Removes a role from a user.
- `./addrole {role_name} [hex_color]`: Creates a new role, optionally with a specified color.
- `./deleterole {role_name}`: Deletes an existing role.
- `./editrole {role_name} [new_name] [new_color]`: Modifies an existing role's name and/or color.

Preconditions:
- The bot instance must be initialized and connected to the Discord server.
- The bot instance must have all role management commands defined.
- The bot must have appropriate permissions to manage roles in the server.
- For user-specific commands, the bot must be able to mention and modify roles for users.

Returns:
- `./roles`: An embed message containing information about all available role management commands.
- `./roleslist`: A paginated embed displaying all roles in the server, their colors, and members.
- Other commands: Confirmation messages for successful actions or error messages for failures.

Raises:
- Various exceptions may be raised and caught within the functions, with error messages sent to the user.

Note:
- The `./roles` command uses a Discord embed to present information in an organized manner.
- `./roleslist` implements pagination with reaction-based navigation for better user experience.
- `./addrole` attempts to position new roles above a 'Pledged' role if it exists.
- `./editrole` can modify both the name and color of a role in a single command.
- Error handling is implemented for most commands to provide feedback on failures.
- The functions demonstrate advanced Discord API usage, including role management and embed manipulation.
- Permissions are not explicitly checked within these functions, relying on Discord's built-in permission system.
"""

def bot_modif_roles(bot):
    # Define the role command 
    @bot.command() 
    async def roles(ctx):
        # Define multiple embed pages 
        embeds = [
            discord.Embed(title = "Roles Commands", description = "Role commands.", color = discord.Color.orange()),
        ]
        
        embeds[0].add_field(name = "./roles", value = "Show roles commands.", inline = True)
        embeds[0].add_field(name="./roleslist", value="Show all roles.", inline=True)
        embeds[0].add_field(name="./editrole", value="./cmnd {role_name} {color} {new_name}", inline=True)
        embeds[0].add_field(name="./addrole", value="Add a role.", inline=True)
        embeds[0].add_field(name="./deleterole", value="Delete a role.", inline=True)
        embeds[0].add_field(name="./setrole", value="./cmnd {@user} {role_name}", inline=True)
        embeds[0].add_field(name="./removerole", value="Remove a role.", inline=True)
        
        await ctx.send(embed = embeds[0])
        
    @bot.command()
    async def setrole(ctx, member: discord.Member, role: discord.Role):
        try:
            if role not in member.roles:
                await member.add_roles(role)
                await ctx.send(f"Role '{role.name}' added to {member.mention}.")
            else:
                await ctx.send(f"{member.mention} already has the role '{role.name}'.")
        except Exception as e:
            await ctx.send(f"Failed to add role '{role.name}' to {member.mention}. Error: {str(e)}")
            
    @bot.command()
    async def removerole(ctx, member: discord.Member, role: discord.Role):
        try:
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Role '{role.name}' removed from {member.mention}.")
            else:
                await ctx.send(f"{member.mention} does not have the role '{role.name}'.")
        except Exception as e:
            await ctx.send(f"Failed to remove role '{role.name}' from {member.mention}. Error: {str(e)}")
        
    @bot.command()
    async def roleslist(ctx):
        roles = ctx.guild.roles
        per_page = 5  # Maximum roles per page

        # Filter out the @everyone role and prepare pages
        filtered_roles = [role for role in roles if role.name != "@everyone"]
        pages = [filtered_roles[i:i + per_page] for i in range(0, len(filtered_roles), per_page)]
        
        # Function to create a single page embed
        def make_embed(page_roles):
            embed = discord.Embed(title="Roles List", color=discord.Color.orange())
            for role in page_roles:
                role_color = str(role.color).upper()
                members_with_role = [member.mention for member in role.members]
                members = ", ".join(members_with_role) if members_with_role else "No members with this role."
                embed.add_field(
                    name=f"{role.name} ({role_color})",
                    value=f"Color: {role_color}\nMembers: {members}",
                    inline=False
                )
            return embed
        
        # Sending the initial page
        current_page = 0
        message = await ctx.send(embed=make_embed(pages[current_page]))
        
        # Add reactions to the message for navigation
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        # Reaction-based pagination
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id

        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction.emoji) == "➡️" and current_page < len(pages) - 1:
                    current_page += 1
                    await message.edit(embed=make_embed(pages[current_page]))
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "⬅️" and current_page > 0:
                    current_page -= 1
                    await message.edit(embed=make_embed(pages[current_page]))
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break
    
    # CHANGE THIS TO WORK WITH EVERY SERVER AND NOT JUST ACRYPT SERVER 
    @bot.command()
    async def addrole(ctx, role_name: str, hex_color: str = None):
        guild = ctx.guild
        color = discord.Color.default()
        
        if hex_color:  # Check if a hex color code was provided
            try:
                color = discord.Color(int(hex_color, 16))  # Convert hex string to a discord.Color
            except ValueError:
                await ctx.send("Invalid hex color. Please use a hex code and remove the # (e.g., 'FF5733').")
                return

        # Create the role
        role = await guild.create_role(name=role_name, color=color)

        # Find the 'Pledged' role and adjust the new role's position if needed
        try:
            pledged_role = discord.utils.get(guild.roles, name="Pledged")
            if pledged_role:
                # Place the new role above 'Pledged'
                await role.edit(position=pledged_role.position + 1)
                await ctx.send(f"Role '{role_name}' created with color {color}.")
            else:
                await ctx.send(f"Role '{role_name}' created with color {color}.")
        except Exception as e:
            await ctx.send(f"Failed to adjust role position or create role. Error: {str(e)}")

    @bot.command()
    async def deleterole(ctx, role: discord.Role):
        try:
            await role.delete()
            await ctx.send(f"Role '{role.name}' gone now.")
        except Exception as e:
            await ctx.send(f"Failed to delete role '{role.name}'. Error: {str(e)}")
    
    @bot.command()
    async def editrole(ctx, role: discord.Role, first_param: str = None, second_param: str = None):
        try:
            updates = {}
            old_name = role.name

            # If both parameters are provided, determine which one is color
            if first_param:
                # Try to check if first_param is a valid hex color
                if first_param.startswith("#") and len(first_param) == 7:
                    try:
                        updates["color"] = discord.Color.from_str(first_param)
                    except ValueError:
                        await ctx.send(f"Invalid color format '{first_param}'. Please provide a valid hex code and remove the # (e.g., #FF5733).")
                        return
                else:
                    updates["name"] = first_param

            # If the second parameter is provided, check if it's a valid color
            if second_param:
                if second_param.startswith("#") and len(second_param) == 7:
                    try:
                        updates["color"] = discord.Color.from_str(second_param)
                    except ValueError:
                        await ctx.send(f"Invalid color format '{second_param}'. Please provide a valid hex code and remove the # (e.g., #FF5733).")
                        return
                else:
                    if "name" in updates:
                        await ctx.send("Too many name changes bro. Please only provide one new name.")
                        return
                    updates["name"] = second_param

            # Apply changes if there are updates
            if updates:
                await role.edit(**updates)
                name_update = f"renamed to '{updates.get('name', old_name)}'" if "name" in updates else ""
                color_update = f"and color changed" if "color" in updates else ""
                await ctx.send(f"Role '{old_name}' {name_update} {color_update}.")
            else:
                await ctx.send(f"No changes made to role '{role.name}'. Please provide a valid color or new name.")
        except Exception as e:
            await ctx.send(f"Failed to edit role '{role.name}'. Error: {str(e)}")