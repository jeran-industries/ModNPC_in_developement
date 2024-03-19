import os
import json
import sqlite3
from datetime import datetime
import aiosqlite

#own modules:
from automod import automod

#messages:
async def messagesenteventlog(message):
    eventtype = "sent" 
    connection = await aiosqlite.connect("./database/database.db")
    #file_name = "./Logs/Messages/V1/" + str(message.guild.id) + '/' + str(message.channel.id) + ".json"
    #print(file_name)
    #if os.path.exists(file_name):
    #    new_data =  {
    #                    'eventtype': eventtype,
    #                    'author_id': message.author.id,
    #                    'author_name': message.author.name,
    #                    'content': message.content,
    #                    'message_id': message.id,
    #                    'timestamp': str(message.created_at)
    #                }
    #    with open(file_name, 'r', encoding = 'utf-8') as f:
    #        data = json.load(f) #loading the data in python for processing
    #    
    #    data["messages"].append(new_data) #adding the new data in the already existing data
    #    with open(file_name, 'w', encoding='utf-8') as f:
    #        json.dump(data, f, indent = 1)
    #        f.close()
    #
    #else: #json file isnt created yet so the bot creates a file.
    #    with open(file_name, 'a', encoding = 'utf-8') as f: #creating file
    #        data = { #new data for the json-file
    #            "messages": [
    #                {
    #                    'eventtype': eventtype,
    #                    'author_id': message.author.id,
    #                    'author_name': message.author.name,
    #                    'content': message.content,
    #                    'message_id': message.id,
    #                    'timestamp': str(message.created_at)
    #                }
    #            ]
    #        }
    #        json.dump(data, f, indent=1) #writing data into json-file
    #        f.close()
    #v2:
    #write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.created_at))

def messageeditedeventlog(message):
    eventtype = "edited"
    #v2:
    #write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.edited_at))

def messagedeletedeventlog(message):
    eventtype="deleted"
    #v1:
    #file_name = "./Logs/Messages/V1/" + str(message.guild.id) + '/' + str(message.channel.id) + ".json"
    ##print(file_name)
    #if os.path.exists(file_name):
    #    new_data =  {
    #                    'eventtype': eventtype,
    #                    'author_id': message.author.id,
    #                    'author_name': message.author.name,
    #                    'content': message.content,
    #                    'message_id': message.id,
    #                    'timestamp': str(message.created_at)
    #                }
    #    with open(file_name, 'r', encoding = 'utf-8') as f:
    #        data = json.load(f) #loading the data in python for processing
    #    
    #    data["messages"].append(new_data) #adding the new data in the already existing data
    #    with open(file_name, 'w', encoding='utf-8') as f:
    #        json.dump(data, f, indent = 1)
    #        f.close()
    
    #else: #json file isnt created yet so the bot creates a file.
    #    with open(file_name, 'a', encoding = 'utf-8') as f: #creating file
    #        data = { #new data for the json-file
    #            "messages": [
    #                {
    #                    'eventtype': eventtype,
    #                    'author_id': message.author.id,
    #                    'author_name': message.author.name,
    #                    'content': message.content,
    #                    'message_id': message.id,
    #                    'timestamp': str(message.created_at)
    #                }
    #            ]
    #        }
    #        json.dump(data, f, indent=1) #writing data into json-file
    #        f.close()
    #v2:
    write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.created_at))

def write_into_log(eventtype, memberid, guildid, channelid, messageid, content, timestamp):
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name) #connect to polldatabase
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messagelog (eventtype TEXT, memberid INTEGER, guildid INTEGER, channelid INTEGER, messageid INTEGER, content TEXT, timestamp TEXT)") #creates a table that have the ground data of the poll
    cursor.execute("INSERT INTO messagelog VALUES (?, ?, ?, ?, ?, ?, ?)", (eventtype, memberid, guildid, channelid, messageid, content, timestamp)) #write into the table the data
    connection.commit()
    connection.close()

#voicechat
async def voicechatupdate(member, before, after): #nennt_mich_wie_ihr_wollt | <VoiceState self_mute=False self_deaf=False self_stream=False suppress=False requested_to_speak_at=None channel=<VoiceChannel id=1128824579398307923 name='Allgemein' rtc_region=None position=0 bitrate=64000 video_quality_mode=<VideoQualityMode.auto: 1> user_limit=0 category_id=1128824579398307920>> | <VoiceState self_mute=False self_deaf=False self_stream=False suppress=False requested_to_speak_at=None channel=None>    
    print(f"{member} | {before} | {after}")

#member
async def memberjoin(member):
    pass

async def memberleave(payload):
    pass

async def memberupdate(before, after):
    pass

async def memberban(guild, user):
    pass

async def memberunban(guild, user):
    pass