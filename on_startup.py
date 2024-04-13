import os
import json
import discord
import io
import sqlite3

#own modules:
from sqlitehandler import insert_into_guildtable, check_4_guild, create_guildsetup_table

async def database_checking_and_creating(bot, guildid):
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS memberlog (guildid INTEGER, memberid INTEGER, timestamp TEXT, status TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS welcomemessagetable (guildid INTEGER, channelid INTEGER, header TEXT, content TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS selfrolesdata (guildid INTEGER, messageid INTEGER, dropdown BOOL, color TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS selfroleoptions (messageid INTEGER, emoji TEXT, roleid TEXT, description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS polldata (messageid INTEGER, channelid INTEGER, guildid INTEGER, votecount INTEGER, runningstatus BOOLEAN)") #creates a table that have the ground data of the poll
    cursor.execute("CREATE TABLE IF NOT EXISTS polloptions (optioncounter INTEGER, messageid INTEGER, option TEXT)") #creates a table for the options
    cursor.execute("CREATE TABLE IF NOT EXISTS pollreactions (messageid INTEGER, member_id INTEGER, emoji TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS messagelog (eventtype TEXT, memberid INTEGER, guildid INTEGER, channelid INTEGER, messageid INTEGER, content TEXT, timestamp TEXT)") #creates a table that have the ground data of the poll

    if await check_4_guild(bot=bot, guildid=guildid)==False:
        await insert_into_guildtable(bot=bot, guildid=guildid)

    try:
        cursor.execute("ALTER TABLE guildsetup ADD logchannelid INTEGER")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE membertable ADD last_upvote INTEGER")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE selfrolesdata ADD dropdown BOOL")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE selfrolesdata ADD color TEXT")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE selfroleoptions ADD description TEXT")
    except:
        pass

    connection.commit()
    connection.close()

    server_folders(guildid)

    #Setup, where everything will be loaded from
    #server_setup_path = './Setup/' + str(server_id) + ".json"
    #if os.path.exists(server_setup_path):
        #server_folders(server_id)
        #return()
    #else:
        #with open(server_setup_path, 'a', encoding='utf-8') as f:
        #    data = {"data":[
        #        {
        #            "bot_setup_channel_id": '',
        #            "bot_updates_channel_id": '',
        #            "reaction_log_status": '',
        #            "reaction_log_channel_id": '',
        #            "welcome_message_status": '',
        #            "welcome_message": ''
        #        }
        #    ]
        #    }
        #    json.dump(data, f, indent=1)
        #    f.close()

def server_folders(guild_id):
    guild_path_generated_rankcard = './database/rankcards/generated/' + str(guild_id) + "/"
    folderbuilder(guild_path_generated_rankcard)

    guild_path_background_rankcard = './database/rankcards/backgrounds/' + str(guild_id) + "/"
    folderbuilder(guild_path_background_rankcard)

    guild_path_profilepictures_rankcard = './database/rankcards/profilepictures/' + str(guild_id) + "/"
    folderbuilder(guild_path_profilepictures_rankcard)
    
    global_path_generated_rankcard = './database/rankcards/generated/' + str(0) + "/"
    folderbuilder(global_path_generated_rankcard)

    global_path_background_rankcard = './database/rankcards/backgrounds/' + str(0) + "/"
    folderbuilder(global_path_background_rankcard)

    global_path_profilepictures_rankcard = './database/rankcards/profilepictures/' + str(0) + "/"
    folderbuilder(global_path_profilepictures_rankcard)

    #Member
    #guild_path_reactionlog_v1 = './Member/' + str(guild_id) + "/"
    #folderbuilder(guild_path_reactionlog_v1)

    #guild_path_polls_v1 = './Polls/V1/' + str(guild_id) + "/"
    #folderbuilder(guild_path_polls_v1)

    #guild_path_polls_v2 = './Polls/V2/'
    #folderbuilder(guild_path_polls_v2)

    #guild_path_selfroles_v1 = './Selfroles/V1/' + str(guild_id) + "/"
    #folderbuilder(guild_path_selfroles_v1)

    #guild_path_reactionlog_v1 = './Logs/Reactions/V1/' + str(guild_id) + "/"
    #folderbuilder(guild_path_reactionlog_v1)

    #guild_path_messagelog_v1 = './Logs/Messages/V1/' + str(guild_id) + "/"
    #folderbuilder(guild_path_messagelog_v1)

#checking and creating
def folderbuilder(folder_path):
    if os.path.exists(folder_path):
        return()
    else:
        os.makedirs(folder_path)

async def message_back_online(bot):
    announcement_channel_id = 1191732882092339270
    announcement_channel = bot.get_channel(announcement_channel_id)
    announcement = "I'm online and sorry 4 being offline! Ready 4 services!!!"
    await announcement_channel.send(file = discord.File("./txtfiles/changelog.txt"), content=announcement)
    message = await announcement_channel.send(announcement)
    #await message.publish() I.)eGgnHgc<%S&mk

async def beta_message_back_online(bot):
    announcement_channel_id = 1214660942995005500
    announcement_channel = bot.get_channel(announcement_channel_id)
    announcement = "I'm online and sorry 4 being offline! Ready 4 services!!!"
    await announcement_channel.send(file = discord.File("./txtfiles/changelog.txt"), content=announcement)
    message = await announcement_channel.send(announcement)