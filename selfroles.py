#v1: 
#saved with json
#called via commands
#v2:
#saved with sql
#called via slashcommands

import discord
import json
import os
import sqlite3
import aiosqlite

#own modules:
from emoji2role import emoji2role
from link2id import link2serverid, link2channelid, link2messageid
from checks import check4dm

async def create_selfrole(interaction, content, channeltopostin): #create a new reactionrole
    if await check4dm(interaction) == False:
        filename = './database/database.db'
        connection = sqlite3.connect(filename) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS selfrolesdata (guildid INTEGER, messageid INTEGER)")
        embed = discord.Embed(title=f'Selfroles:', description=f'{content}', color=discord.Color.green())
        message = await channeltopostin.send(embed=embed)
        cursor.execute("INSERT INTO selfrolesdata VALUES (?, ?, ?)", (interaction.guild.id, message.id, False)) #write into the table the data
        await interaction.response.send_message("**Success** \nThe reactionrolesmessage was created.", ephemeral=True)
        connection.commit()
        connection.close()

    #bot = ctx.bot
    #message_id = link2messageid(link)   #calls a module so a link become seperated to a message_id
    #channel_id = int(link2channelid(link))   #calls a module so a link become seperated to a channel_id
    #server_id = link2serverid(link)     #calls a module so a link become seperated to a server_id
    #channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    #message = await channel.get_partial_message(message_id).fetch() #getting the message to add a reaction so the user can more easy react
    #await message.add_reaction(emoji) #adding the reaction to message
    #file_name = './Selfroles/V1/' + str(server_id) + '/' + str(message_id) + '.json' #getting the filename
    #if (os.path.exists(file_name)) and (checkifroleexists(ctx,role) == True): #checking if filename already exists
    #    if emoji2role(file_name, emoji) == None: #checking if entry in file already exists
    #        new_data =  { #data that should be added
    #                        "emoji": emoji,
    #                        "role": role
    #                    }
    #        with open(file_name,'r+', encoding = 'utf-8') as f: #open the already existing file
    #            data = json.load(f) #loading the data in python for processing
    #            data["emojis"].append(new_data) #adding the new data in the already existing data
    #            f.seek(0)
    #            json.dump(data, f, indent=1) #saving all the data
    #            f.close()
    #    else: #if entry already exists, exit the command
            #return
    #        errormessage = await interaction.response.send_message("This reactionrole is created or already exists.", ephemeral=True) #empheral doesnt work but nvm i have to work on other things
            #await ctx.delete()
            
    #else: #json file isnt created yet so the bot creates a file.
    #    data = { #new data for the json-file
    #        "emojis": [ 
    #            { 
    #            "emoji": emoji,
    #            "role": role
    #            }
    #        ]
    #    }

    #    with open(file_name, 'a', encoding = 'utf-8') as f: #creating file
    #        json.dump(data, f, indent=1) #writing data into json-file, indent!=0 means that its formated
    #        f.close()

async def add_selfrole(interaction, bot, link, emoji, role, description):
    if await check4dm(interaction) == False and int(interaction.guild.id) == link2serverid(link):
        if checkifroleexists(interaction.guild, role) == True:
            messageid = link2messageid(link)
            filename = './database/database.db'
            connection = sqlite3.connect(filename) #connect to polldatabase
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS selfroleoptions (messageid INTEGER, emoji TEXT, roleid TEXT)")
            if cursor.execute("SELECT * FROM selfroleoptions WHERE messageid = ? AND emoji = ? AND roleid = ?", (messageid, emoji, role.id)).fetchone() is None:
                channel = await bot.fetch_channel(link2channelid(link)) #getting the channel from the message
                message = await channel.fetch_message(messageid)
                embed = message.embeds[0]
                if description == None:
                    embed.add_field(name = f"{emoji} || {role}", value = "", inline = False) #adds a new field to the embedded message for each option
                else:
                    embed.add_field(name = f"{emoji} || {role}", value = description, inline = False) #adds a new field to the embedded message for each option
                await message.edit(embed=embed) #sending all the fields
                await message.add_reaction(emoji) #adding the reaction to message
                cursor.execute("INSERT INTO selfroleoptions VALUES (?, ?, ?)", (messageid, emoji, role.id)) #write into the table the data
            else:
                await interaction.response.send_message("This reactionrole was already added.", ephemeral=True)
        else:
            await interaction.response.send_message("The role isnt created yet or was deleted.", ephemeral=True) #empheral doesnt work but nvm i have to work on other things
        connection.commit()
        connection.close()
    else:
        await interaction.response.send_message("The link to the reactionrolemessage isnt from this server.", ephemeral=True)
        

async def clear_message_from_selfroles(ctx, link): #create a new reactionrole
    bot = ctx.bot
    message_id = link2messageid(link)
    channel_id = int(link2channelid(link))   #calls a module so a link become seperated to a channel_id
    server_id = link2serverid(link)
    channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    message = await channel.get_partial_message(message_id).fetch() #getting the message to add a reaction so the user can more easy react
    await message.clear_reactions()

    file_name = './Selfroles/V1/' +str(server_id) + '/' + str(message_id) + '.json' #getting the filename
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        await ctx.reply('This message has been already cleared or was never a message for reactionroles!')

    
async def add_selfrole_2_member(bot, payload):
    #v2:
    messageid = payload.message_id
    emoji = payload.emoji.name
    memberid = payload.user_id
    if memberid != bot.user.id:
        guild = bot.get_guild(payload.guild_id) #getting guild
        member = guild.get_member(memberid) #getting member
        filename = './database/database.db'
        connection = sqlite3.connect(filename) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS selfroleoptions (messageid INTEGER, emoji TEXT, roleid INTEGER)")
        if cursor.execute("SELECT * FROM selfroleoptions WHERE messageid = ? AND emoji = ?", (messageid, emoji)).fetchone() is not None:        
            cursor.execute("SELECT roleid FROM selfroleoptions WHERE messageid = ? AND emoji = ?", (messageid, emoji))
            roleid = next(cursor, [None])[0]
            role = discord.utils.get(guild.roles, id=roleid)
            if memberid != bot.user.id:
                await member.add_roles(role)
        elif cursor.execute("SELECT * FROM selfroleoptions WHERE messageid = ?", (messageid,)).fetchone() is not None:
            channelid = payload.channel_id
            channel = await bot.fetch_channel(channelid) #getting the channel from the message
            message = await channel.get_partial_message(messageid).fetch() #getting the message to add a reaction so the user can more easy react
            if memberid != bot.user.id:
                await message.remove_reaction(emoji, member)
    #v1:
    #message_id = payload.message_id
    #member_id = payload.user_id
    #server_id = payload.guild_id
    #server = bot.get_guild(payload.guild_id) #getting guild
    #member = server.get_member(member_id) #getting member
    #file_name = './Selfroles/V1/' + str(server_id) + '/' + str(message_id) + '.json' #getting the filename
    #role = emoji2role(file_name, payload.emoji.name) #getting right role
    #if role != None: #is there an emoji role relation?
    #    server_role = discord.utils.get(server.roles, name = role) #getting right role in server
    #    if member_id != bot.user.id: #if there isnt this if-loop, by creating a reactionrole this bot also receives the reactionrole
    #        await member.add_roles(server_role) #adding role to member, Error code: 50013, why? the bot has admin rights => not a syntax problem, the roll of the bot must be higher played than the role of the selfrole

async def remove_selfrole_from_member(bot, payload):
    #v2:
    messageid = payload.message_id
    emoji = payload.emoji.name
    memberid = payload.user_id

    guild = bot.get_guild(payload.guild_id) #getting guild
    member = guild.get_member(memberid) #getting member
    filename = './database/database.db'
    connection = sqlite3.connect(filename) #connect to polldatabase
    cursor = connection.cursor()
    if cursor.execute("SELECT * FROM selfroleoptions WHERE messageid = ? AND emoji = ?", (messageid, emoji)).fetchone() is not None:        
        cursor.execute("SELECT roleid FROM selfroleoptions WHERE messageid = ? AND emoji = ?", (messageid, emoji))
        roleid = next(cursor, [None])[0]
        role = discord.utils.get(guild.roles, id=roleid)
        if memberid != bot.user.id:
            await member.remove_roles(role)

    #v1:
    #message_id = payload.message_id
    #member_id = payload.user_id
    #server = bot.get_guild(payload.guild_id) #getting guild
    #member = server.get_member(member_id) #getting member
    #file_name = './Selfroles/V1/' + str(payload.guild_id) + '/' + str(message_id) + '.json' #getting the filename
    #role = emoji2role(file_name, payload.emoji.name) #getting right role
    #if role != None: #is there an emoji role relation
    #    role = discord.utils.get(server.roles, name = role) #getting right role in guild
    #    await member.remove_roles(role) #removing role from member

#programmingphase:
async def create_selfrole_select_menu(interaction, content, channeltopostin, role, description):
    embed = discord.Embed(title="Get your selfroles with this menu:", description=content, color=0x00ff00)
    message = await channeltopostin.send(embed=embed, view=SelfrolesSelect(role=role, description = description))
    await interaction.response.send_message("**Success** \nThe reactionrolesmessage was created.", ephemeral=True)

class SelfrolesSelectMenu(discord.ui.Select):
    def __init__(self, role, description):
        super().__init__(placeholder="No selfrole yet", options=[discord.SelectOption(label=role.name, value=role.id, description = description)])

    async def callback(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(content=f"Sucessfully given you {self.values}")

class SelfrolesSelect(discord.ui.View):
    def __init__(self, role, description):
        super().__init__()
        self.add_item(SelfrolesSelectMenu(role = role, description = description))

async def add_selfrole_2_select_menu(bot, link, role, description):
    message_id = link2messageid(link)   #calls a module so a link become seperated to a message_id
    channel_id = int(link2channelid(link))   #calls a module so a link become seperated to a channel_id
    server_id = link2serverid(link)     #calls a module so a link become seperated to a server_id
    channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    message = await channel.get_partial_message(message_id).fetch() #getting the message to add a reaction so the user can more easy react    

def checkifroleexists(guild, role):
    for arole in guild.roles:
        if role == arole:
           return(True) 
    return(False)