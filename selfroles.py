#v1: 
#saved with json
#called via commands
#v2:
#saved with sql
#called via slashcommands

import discord
import json
import os
import aiosqlite

#own modules:
from emoji2role import emoji2role
from link2id import link2serverid, link2channelid, link2messageid
from checks import check4dm
from sqlitehandler import insert_into_selfroles, insert_into_selfrole_options, get_selfrole_roleid, check_4_selfrole

async def create_selfrole(interaction, content, channeltopostin): #create a new reactionrole
    if await check4dm(interaction) == False:
        member = interaction.user
        bot = interaction.client
        guildid = interaction.guild.id
        if member.guild_permissions.manage_roles:
            embed = discord.Embed(title=f'Selfroles:', description=f'{content}', color=discord.Color.green())
            message = await channeltopostin.send(embed=embed)

            dropdown = False
            color = None

            await insert_into_selfroles(bot=bot, guildid=guildid, messageid=message.id, dropdown=dropdown, color=color)
            await interaction.response.send_message("**Success** \nThe reactionrolesmessage was created.", ephemeral=True)
        else:
            await interaction.response.send_message("**ERROR** \nYou dont have the permission: `manage roles`.", ephemeral=True)
    else:
        await interaction.response.send_message("**ERROR** \nYou cant use this command outside of servers.", ephemeral=True)

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
            if interaction.user.guild_permissions.manage_roles:
                messageid = link2messageid(link)
                data = await get_selfrole_roleid(bot=bot, messageid=messageid, emoji=emoji)
                if data is None:
                    channel = await bot.fetch_channel(link2channelid(link)) #getting the channel from the message
                    message = await channel.fetch_message(messageid)
                    embed = message.embeds[0]
                    if description == None:
                        embed.add_field(name = f"{emoji} || {role}", value = "", inline = False) #adds a new field to the embedded message for each option
                    else:
                        embed.add_field(name = f"{emoji} || {role}", value = description, inline = False) #adds a new field to the embedded message for each option
                    await message.edit(embed=embed) #sending all the fields
                    await message.add_reaction(emoji) #adding the reaction to message
                    await insert_into_selfrole_options(bot=bot, messageid=messageid, emoji=emoji, roleid=role.id, description=description)
                    await interaction.response.send_message("**SUCCESS** \nReactionrole was added.", ephemeral=True)
                else:
                    await interaction.response.send_message("This reactionrole was already added.", ephemeral=True)
            else:
                await interaction.response.send_message("**ERROR** \nYou dont have the permission: `manage roles`.", ephemeral=True)
        else:
            await interaction.response.send_message("The role isnt created yet or was deleted.", ephemeral=True) #empheral doesnt work but nvm i have to work on other things
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
        roleid = await get_selfrole_roleid(bot=bot, messageid=messageid, emoji=emoji)
        if roleid is not None:        
            role = discord.utils.get(guild.roles, id=roleid)
            if memberid != bot.user.id:
                await member.add_roles(role)
        elif await check_4_selfrole(bot=bot, messageid=messageid) == True:
            channelid = payload.channel_id
            channel = await bot.fetch_channel(channelid) #getting the channel from the message
            message = await channel.get_partial_message(messageid).fetch() #getting the message to add a reaction so the user can more easy react
            if memberid != bot.user.id:
                await message.remove_reaction(emoji, member)
        #else:
        #    channelid = payload.channel_id
        #    channel = await bot.fetch_channel(channelid) #getting the channel from the message
        #    await channel.send(f"<@{memberid}> There is an error due to problems saving the data in the database. Please ask the staff of the server to redo the reactionroles.")
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
    roleid = await get_selfrole_roleid(bot=bot, messageid=messageid, emoji=emoji)
    if roleid is not None:        
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
async def create_selfrole_select_menu(bot, interaction, content, channeltopostin, emoji, role, description):
    embed = discord.Embed(title="Selfroles:", description=f"{content}")
    followup = await interaction.response.defer(ephemeral = True)
    guild = interaction.guild
    message = await channeltopostin.send(embed=embed, view=SelfrolesSelect(emoji=emoji, role=role, description = description))
    #bot.add_view(SelfrolesSelect())
    connection = await aiosqlite.connect("./database/database.db")
    await connection.execute("INSERT INTO selfrolesdata VALUES (?, ?, ?, ?)", (guild.id, message.id, True, None)) #saving data
    await connection.execute("INSERT INTO selfroleoptions VALUES (?, ?, ?, ?)", (message.id, emoji, role.id, description)) #saving data
    await connection.commit()
    await connection.close()
    await interaction.response.send_message("**Success** \nThe reactionrolesmessage was created.", ephemeral=True)

class SelfrolesSelect(discord.ui.View):
    def __init__(self, emoji, role, description):
        super().__init__(timeout=None)
        self.add_item(SelfrolesSelectMenu(emoji = emoji, role = role, description = description))

class SelfrolesSelectMenu(discord.ui.Select):
    def __init__(self, emoji, role, description):
        options =   [
                    discord.SelectOption(label=role.name, value=role.id, emoji=emoji, description = description),
                    ]
        super().__init__(placeholder="Choose your selfroles in this dropdownmenu", max_values=1, options=options, custom_id = "SelfrolesSelectMenu")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        for value in self.values:
            roleid = int(value)
            role = guild.get_role(roleid)
            memberrole = member.get_role(roleid)
            if memberrole == None:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

async def add_selfrole_2_select_menu(bot, link, emoji, role, description):
    message_id = link2messageid(link)   #calls a module so a link become seperated to a message_id
    channel_id = int(link2channelid(link))   #calls a module so a link become seperated to a channel_id
    server_id = link2serverid(link)     #calls a module so a link become seperated to a server_id
    channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    message = await channel.get_partial_message(message_id).fetch() #getting the message to add a reaction so the user can more easy react 
    connection = await aiosqlite.connect("./database/database.db")  

async def selfrolesaddview(bot):
    connection = await aiosqlite.connect("./database/database.db")
    messageidscursor = await connection.execute('SELECT messageid FROM selfrolesdata WHERE dropdown = ? AND memberid = ?', (True,))
    messageids = await messageidscursor.fetchall()
    await messageidscursor.close()
    for messageid in messageids:
        emojicursor = await connection.execute('SELECT emoji FROM selfroleoptions WHERE messageid = ?', (messageid,))
        emojilist = await emojicursor.fetchone()
        await emojicursor.close()
        rolecursor = await connection.execute('SELECT role FROM selfroleoptions WHERE messageid = ?', (messageid,))
        rolelist = await rolecursor.fetchone()
        await rolecursor.close()
        descriptioncursor = await connection.execute('SELECT role FROM selfroleoptions WHERE messageid = ?', (messageid,))
        descriptionlist = await descriptioncursor.fetchone()
        await descriptioncursor.close()
        for emoji, role, description in emojilist, rolelist, descriptionlist:
            bot.add_view(SelfrolesSelect(emoji, role, description)) 

def checkifroleexists(guild, role):
    for arole in guild.roles:
        if role == arole:
           return(True) 
    return(False)