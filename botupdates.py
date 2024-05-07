import discord
import sqlite3


#U need a botupdateschannel to use the bot. 
#Command to set the botupdatechannel:
#moved to ./setup.py
#async def setbotupdateschannelcommand(interaction, channel):
#    file_name = "./database/database.db"
#    connection = sqlite3.connect(file_name) #connect to polldatabase
#    cursor = connection.cursor()
#    cursor.execute("UPDATE guildsetup set botupdatechannelid = ?", (channel.id,))
#    embed = discord.Embed(title=f'Success', description=f"The botupdatechannel was set to {channel}. All commands can be now used.", color=discord.Color.green())
#    await interaction.response.send_message(embed = embed)


#command to send botupdates to the botupdateschannel
async def publishbotupdatescommand(interaction, bot, botupdatemessage): #only 4 Member of developerteam
    member = interaction.user
    permitteduser = [945785058676072448]
    for i in permitteduser:
        if member.id == permitteduser[i]:
            embed = discord.Embed(title=f'Running Botupdate...', description=f"Running Botupdate...", color=discord.Color.green())
            await interaction.response.send_message(embed = embed)
            file_name = "./database/database.db"
            connection = sqlite3.connect(file_name)
            cursor = connection.cursor()
            guildids = cursor.execute("SELECT guildid FROM guildsetup")
            for guildid in guildids:
                botupdatechannelid = cursor.execute("SELECT botupdatechannelid FROM guildsetup WHERE guildid = ?", (guildid,))
                botupdatechannel = await bot.fetch_channel(botupdatechannelid)
                embedbotupdate = discord.Embed(title=f'New Botupdate', description=f"Running Botupdate...", color=discord.Color.green())
                botupdatechannel.send(embed = embedbotupdate)
                return()
    embed = discord.Embed(title=f'Attention', description=f"You aren't allowed to use this command!!!", color=discord.Color.dark_red())
    await interaction.response.send_message(embed = embed)