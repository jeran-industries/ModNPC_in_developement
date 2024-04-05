import sqlite3
import discord

#own modules:
from sqlitehandler import asqlite_pull_data,asqlite_insert_data,asqlite_update_data

async def sendwelcomemessage(member, bot):
    #file_name = "./database/database.db"
    #connection = sqlite3.connect(file_name)
    #cursor = connection.cursor()
    guildid = member.guild.id
    channelid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guildid}", data_to_return="channelid")
    if channelid is not None:
        #cursor.execute("SELECT channelid FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        #channel_id = next(cursor, [None])[0]
        #cursor.execute("SELECT header FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        #welcomemessageheader = next(cursor, [None])[0]
        #cursor.execute("SELECT content FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        #welcomemessagecontent = next(cursor, [None])[0]
        
        welcomemessageheader = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guildid}", data_to_return="header")
        welcomemessagecontent = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guildid}", data_to_return="content")

        embed = discord.Embed(title=f'{welcomemessageheader}', description=f'{welcomemessagecontent}', color=discord.Color.green())
        channel = await bot.fetch_channel(channelid) #getting the channel from the message
        await channel.send(embed = embed)

    #add support for editing welcomemessage
    #{member.mention} doesnt work yet.