import discord

#own modules:
from sqlitehandler import asqlite_pull_data,asqlite_insert_data,asqlite_update_data

async def sendwelcomemessage(bot, interaction=None, member=None):
    #file_name = "./database/database.db"
    #connection = sqlite3.connect(file_name)
    #cursor = connection.cursor()
    if member is None:
        member=interaction.user
        guild = interaction.guild
    else:
        guild = member.guild
    channelid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guild.id}", data_to_return="channelid")

    if channelid is not None:
        #cursor.execute("SELECT channelid FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        #channel_id = next(cursor, [None])[0]
        #cursor.execute("SELECT header FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        #welcomemessageheader = next(cursor, [None])[0]
        #cursor.execute("SELECT content FROM welcomemessagetable WHERE guildid = ?", (guildid,))
        #welcomemessagecontent = next(cursor, [None])[0]
        
        welcomemessageheader = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guild.id}", data_to_return="header")
        welcomemessagecontent = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guild.id}", data_to_return="content")
        welcomemessagethumbnailtype = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guild.id}", data_to_return="thumbnailtype")

        welcomemessageheader = welcomemessageheader.replace("{member.mention}", member.mention)
        welcomemessageheader = welcomemessageheader.replace("{member.name}", member.name)
        welcomemessageheader = welcomemessageheader.replace("{member.display_name}", member.display_name)
        
        welcomemessagecontent = welcomemessagecontent.replace("{member.mention}", member.mention)
        welcomemessagecontent = welcomemessagecontent.replace("{member.name}", member.name)
        welcomemessagecontent = welcomemessagecontent.replace("{member.display_name}", member.display_name)

        embed = discord.Embed(title=f'{welcomemessageheader}', description=f'{welcomemessagecontent}', color=discord.Color.green())
        if welcomemessagethumbnailtype == "userpfp":
            avatar_url = member.avatar.url if member.avatar else None
            if avatar_url:
                embed.set_thumbnail(url=avatar_url)
            #embed.set_image(url="attachment://image.png")
            #os.remove(f"./database/rankcards/profilepictures/{guild.id}/{member.id}.png")
        elif welcomemessagethumbnailtype == "servericon":
            icon_url = guild.icon.url if guild.icon else None
            if icon_url:
                embed.set_thumbnail(url=icon_url)
        
        channel = await bot.fetch_channel(channelid) #getting the channel from the message
        if interaction is None:
            await channel.send(content=member.mention, embed = embed)
        else:
            await interaction.response.send_message(content=member.mention, embed = embed)

    #add support for editing welcomemessage
    #{member.mention} doesnt work yet.