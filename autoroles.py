import discord
import asyncio

#own modules:
from checks import check4dm, check4role
from sqlitehandler import get_autoroles

async def add_autorole_2_user(bot, member):
    roles = []
    guild = member.guild
    guildid = guild.id

    #print("\n Im here \n")

    ##all(0) usergroups: bot(1) and humanusers(2)
    membergroup = 0
    await membergrouproleassignement(guild, membergroup, member, bot)

    #botusers:
    if member.bot == True:
        membergroup = 1
        await membergrouproleassignement(guild, membergroup, member, bot)

    #humanusers:
    else:
        membergroup = 2
        await membergrouproleassignement(guild, membergroup, member, bot)

async def membergrouproleassignement(guild, membergroup, member, bot):

    roleidsmembergroupusers = await get_autoroles(bot=bot, guildid=guild.id, membergroup=membergroup)

    roles = []
    if roleidsmembergroupusers != []:
        roles = await getroles(roles=roles, roleids=roleidsmembergroupusers, guild=guild, member=member)


async def addrole2allmembercommand(interaction, role, membergroup):
    if await check4dm(interaction) == False:
        guild = interaction.guild
        member = interaction.user
        channel = interaction.channel
        if member.guild_permissions.manage_roles:
            i = 0
            for guildmember in guild.members:
                if membergroup == 0:
                    if await check4role(guildmember, role) == False:
                        i = i + 1
                elif membergroup == 1:
                    if guildmember.bot == True:
                        if await check4role(guildmember, role) == False:
                            i = i + 1
                elif membergroup == 2:
                    if guildmember.bot == False:
                        if await check4role(guildmember, role) == False:
                            i = i + 1
            if membergroup == 0:
                loadingembed = discord.Embed(title=f'LOADING', description = f'Adding the role to all users. This will take about {i} seconds.', color=discord.Color.yellow())
            elif membergroup == 1:
                loadingembed = discord.Embed(title=f'LOADING', description = f'Adding the role to all botusers. This will take about {i} seconds.', color=discord.Color.yellow())
            elif membergroup == 2:
                loadingembed = discord.Embed(title=f'LOADING', description = f'Adding the role to all humanusers. This will take about {i} seconds.', color=discord.Color.yellow())
            await interaction.response.send_message(embed = loadingembed, ephemeral = True, delete_after = i)
            for guildmember in guild.members:
                if membergroup == 0:
                    if await check4role(guildmember, role) == False:
                        await guildmember.add_roles(role)
                        await asyncio.sleep(1)
                elif membergroup == 1:
                    if guildmember.bot == True:
                        if await check4role(guildmember, role) == False:
                            await guildmember.add_roles(role)
                            await asyncio.sleep(1)
                elif membergroup == 2:
                    if guildmember.bot == False:
                        if await check4role(guildmember, role) == False:
                            await guildmember.add_roles(role)
                            await asyncio.sleep(1)
            successembed = discord.Embed(title=f'SUCCESS', description = f'Adding role completed', color=discord.Color.green())
            await channel.send(embed=successembed)
        else:
            errorembed = discord.Embed(title=f'ERROR', description = f'You dont have the rights to do that', color=discord.Color.red())
            await interaction.response.send_message(embed = errorembed, ephemeral = True)

async def removerolefromallmembercommand(interaction, role, membergroup):
    if await check4dm(interaction) == False:
        guild = interaction.guild
        member = interaction.user
        channel = interaction.channel
        if member.guild_permissions.manage_roles:
            i = 0
            for guildmember in guild.members:
                if membergroup == 0:
                    if await check4role(guildmember, role) == True:
                        i = i + 1
                elif membergroup == 1:
                    if guildmember.bot == True:
                        if await check4role(guildmember, role) == True:
                            i = i + 1
                elif membergroup == 2:
                    if guildmember.bot == False:
                        if await check4role(guildmember, role) == True:
                            i = i + 1
            if membergroup == 0:
                loadingembed = discord.Embed(title=f'LOADING', description = f'Removing the role from all users. This will take about {i} seconds.', color=discord.Color.yellow())
            elif membergroup == 1:
                loadingembed = discord.Embed(title=f'LOADING', description = f'Removing the role from all botusers. This will take about {i} seconds.', color=discord.Color.yellow())
            elif membergroup == 2:
                loadingembed = discord.Embed(title=f'LOADING', description = f'Removing the role from all humanusers. This will take about {i} seconds.', color=discord.Color.yellow())
            await interaction.response.send_message(embed = loadingembed, ephemeral = True, delete_after = i)
            for guildmember in guild.members:
                if membergroup == 0:
                    if await check4role(guildmember, role) == True:
                        await guildmember.remove_roles(role)
                        await asyncio.sleep(1)
                elif membergroup == 1:
                    if guildmember.bot == True:
                        if await check4role(guildmember, role) == True:
                            await guildmember.remove_roles(role)
                            await asyncio.sleep(1)
                elif membergroup == 2:
                    if guildmember.bot == False:
                        if await check4role(guildmember, role) == True:
                            await guildmember.remove_roles(role)
                            await asyncio.sleep(1)
            successembed = discord.Embed(title=f'SUCCESS', description = f'Removing roles completed', color=discord.Color.green())
            await channel.send(embed=successembed)
        else:
            errorembed = discord.Embed(title=f'ERROR', description = f'You dont have the rights to do that', color=discord.Color.red())
            await interaction.response.send_message(embed = errorembed, ephemeral = True)
        
async def getroles(roles, roleids, guild, member):
    for roleid in roleids:
        roleid = roleid[0]
        if roleid is None:
            if roles == []:
                roles = None
            return(roles)
        elif roleid == []:
            pass
        else:
            role = guild.get_role(roleid)
            if role.is_assignable():
                roles.append(role)
                await member.add_roles(role)

    if roles == []:
        roles = None
    return(roles)