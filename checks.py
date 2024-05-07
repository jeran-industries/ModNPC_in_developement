import sqlite3
import discord
import requests
import json
from datetime import datetime

from sqlitehandler import update_lastupvote, change_xp_by, get_lastupvote

def check4premium(guildid):
    pass

#Errormessage/Control if botupdatechannel is set
async def check4botupdatechannel(interaction):
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name)
    cursor = connection.cursor()
    cursor.execute("SELECT botupdatechannelid FROM guildsetup WHERE guildid = ?", (interaction.guild.id,))
    botupdatechannelid = next(cursor, [None])[0]
    connection.close()
    if botupdatechannelid == None: #or the channel doesnt exist anymore
        embed = discord.Embed(title=f'Attention', description=f"For using this bot, the staff must set a botupdatechannel. They can set it with this slashcommand: `/setbotupdatechannelcommand`. If you set one and there is an error, join the supportserver.", color=discord.Color.red())
        await interaction.response.send_message(embed = embed)
        return(False)
    else:
        return(True)
    
async def check4role(member, role):
    for role4check in member.roles:
        if role4check.id == role.id:
            return(True)
    return(False)

async def check4dm(interaction):
    membername = interaction.user.name
    if str(interaction.channel) == f"Direct Message with {membername}":
        embed = discord.Embed(title=f'Error', description=f"You can't use this command in direct messages.", color=discord.Color.red())
        await interaction.response.send_message(embed = embed)
        return(True)
    else:
        return(False)

async def check4dm_message(message):
    print(str(message.channel))
    if str(message.channel)[0-13] == "Direct Message":
        return(True)
    else:
        return(False)

async def check4upvotebotlist(bot, botlisttoken):
    botid = 1144006301765095484
    url = f"https://discordbotlist.com/api/bots/{botid}/upvotes"
    headers = {
        "Authorization": f"{botlisttoken}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        botlistupvotes = response.json()["upvotes"]
        for botlistupvote in botlistupvotes:
            memberid = botlistupvote["user_id"]

            timelastupvote = await get_lastupvote(bot=bot, guildid=0, memberid=memberid)

            if timelastupvote is not None:
                time = int(round((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
                if time-timelastupvote >= 43200:

                    await update_lastupvote(bot=bot, time=time, guildid=0, memberid=memberid)

                    await change_xp_by(bot=bot, guildid=0, memberid=memberid, xptomodify=100)
                        
    else:
        print(f"ERROR Botlist has answered with:{response.status_code}")

async def check4permission():
    pass