import sqlite3
import discord

async def sendwelcomemessage(interaction, member, bot):
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name)
    cursor = connection.cursor()
    guildid = member.guild.id
    if (cursor.execute("SELECT * FROM welcomemessagetable WHERE guildid = ?", (guildid,)).fetchone() is not None):
        cursor.execute("SELECT channelid FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        channel_id = next(cursor, [None])[0]
        cursor.execute("SELECT header FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        welcomemessageheader = next(cursor, [None])[0]
        cursor.execute("SELECT content FROM welcomemessages WHERE guildid = ?", (guildid,))
        welcomemessagecontent = next(cursor, [None])[0]
        embed = discord.Embed(title=f'{welcomemessageheader}', description=f'{welcomemessagecontent}', color=discord.Color.green())
        channel = await bot.fetch_channel(channel_id) #getting the channel from the message
        await channel.send(embed = embed)