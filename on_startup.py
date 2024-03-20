import os
import json
import discord
import io
import sqlite3

def database_checking_and_creating(guildid):
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS guildsetup (guildid INTEGER, levelingsystemstatus BOOL, levelingpingmessagechannel INTEGER, welcomemessagestatus BOOL, anonymousmessagecooldown INTEGER, anonymousmessagecooldown BOOL, botupdatestatus BOOL, botupdatechannelid INTEGER)")
    if (cursor.execute("SELECT * FROM guildsetup WHERE guildid = ?", (guildid,)).fetchone()) is None:
        cursor.execute("INSERT INTO guildsetup VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (guildid, False, None, False, None, False, False, None)) #saving data
    try:
        cursor.execute("ALTER TABLE membertable ADD last_upvote INTEGER")
        cursor.execute("ALTER TABLE selfrolesdata ADD dropdown BOOL")
        cursor.execute("ALTER TABLE selfrolesdata ADD color BOOL")
    except:
        pass

    connection.commit()
    connection.close()
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
    #Member
    guild_path_reactionlog_v1 = './Member/' + str(guild_id) + "/"
    folderbuilder(guild_path_reactionlog_v1)

    guild_path_polls_v1 = './Polls/V1/' + str(guild_id) + "/"
    folderbuilder(guild_path_polls_v1)

    guild_path_polls_v2 = './Polls/V2/'
    folderbuilder(guild_path_polls_v2)

    guild_path_selfroles_v1 = './Selfroles/V1/' + str(guild_id) + "/"
    folderbuilder(guild_path_selfroles_v1)

    guild_path_reactionlog_v1 = './Logs/Reactions/V1/' + str(guild_id) + "/"
    folderbuilder(guild_path_reactionlog_v1)

    guild_path_messagelog_v1 = './Logs/Messages/V1/' + str(guild_id) + "/"
    folderbuilder(guild_path_messagelog_v1)

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