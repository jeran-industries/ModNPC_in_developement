import discord
import sqlite3
import datetime

async def sendanonymousmessagecommand(interaction, message, channel):
    filename = "./database/database.db"
    connection = sqlite3.connect(filename) 
    cursor = connection.cursor()
    cursor.execute("SELECT anonymousmessagestatus FROM guildsetup WHERE guildid = ?", (interaction.guild.id,))
    anonymousmessagestatus = next(cursor, [None])[0] #looks up if anonymousmessages are allowed on this server
    if anonymousmessagestatus == 1:
        cursor.execute("SELECT anonymousmessagecooldown FROM guildsetup WHERE guildid = ?", (interaction.guild.id,))
        cooldown = next(cursor, [None])[0] #looks how big the cooldown is on this server
        cursor.execute("SELECT anonymousmessagecooldown FROM membertable WHERE guildid = ?", (interaction.guild.id,))
        lastmessage = next(cursor, [None])[0] #looks how big the cooldown is on this server
        current_date = datetime.datetime.now()
        current_time = current_date.year*10000000000 + current_date.month*100000000 + current_date.day*1000000 + current_date.hour*10000 + current_date.minute*100 + current_date.second
        if current_time - cooldown >= lastmessage:
        #checks if there is a cooldown on this member        
            if channel.permissions_for(interaction.user).send_messages:
                cursor.execute("UPDATE membertable set lastanonymousmessagetimestamp = ? WHERE guildid = ? AND memberid = ?", (current_time, interaction.guild.id, interaction.user.id))
                anonymousembed = discord.Embed(title=f'Someone sent an anonymous message:', description = f"||{message}||", color=discord.Color.light_grey())
                await channel.send(embed = anonymousembed)
                successembed = discord.Embed(title=f'Success!!!', description = f'Your message "{message}" was posted in {channel}', color=discord.Color.gold())
                await interaction.response.send_message(embed = successembed, ephemeral = True)
            else:
                misssuccessembed = discord.Embed(title=f'Error', description = f'Your message "{message}" cant be posted in {channel} because of missing permissions', color=discord.Color.dark_red())
                await interaction.response.send_message(embed = misssuccessembed, ephemeral = True)
        else:
            misssuccessembed = discord.Embed(title=f'Error', description = f'There is a cooldown on anonymous messages. You can use it again in {current_time - cooldown}', color=discord.Color.dark_red())
            await interaction.response.send_message(embed = misssuccessembed, ephemeral = True)
    else:
        misssuccessembed = discord.Embed(title=f'Error', description = f'This feature isnt activated yet by the moderators of this server', color=discord.Color.dark_red())
        await interaction.response.send_message(embed = misssuccessembed, ephemeral = True)
    connection.commit()
    connection.close()

#async def anonymouscommandsetup(interaction, cooldown):
#    member = interaction.user
#    if member.guild_permissions.administrator:
#        filename = "./database/database.db"
#        connection = sqlite3.connect(filename)
#        cursor = connection.cursor()
#        cursor.execute("UPDATE guildsetup set anonymousmessagestatus = ? WHERE guildid = ?", (True, interaction.guild.id))
#        cursor.execute("UPDATE guildsetup set anonymousmessagecooldown = ? WHERE guildid = ?", (cooldown, interaction.guild.id))
#        connection.commit()
#        connection.close()
#    else:
#        misssuccessembed = discord.Embed(title=f'Error', description = f'You dont have the rights to do that', color=discord.Color.dark_red())
#        await interaction.response.send_message(embed = misssuccessembed, ephemeral = True)

async def anonymousloglookup(interaction, messageid):
    
    pass