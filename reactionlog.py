import json
import os
import io
import datetime
import sqlite3

async def new_reaction_4_log(payload, bot):
    #channel_id = payload.channel_id
    #channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    message_id = payload.message_id
    #message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react 
    server_id = payload.guild_id
    #server = bot.get_guild(payload.guild_id) #getting guild
    member_id = payload.user_id #getting member
    #member = server.get_member(member_id)
    #reactions = message.reactions
    emoji = payload.emoji.name    
    time = str(datetime.datetime.now(datetime.timezone.utc))
    eventtype = "reaction_added"
    file_name = "./Logs/Reactions/V1/" + str(server_id) + "/" + str(message_id) + ".json"
    if os.path.exists(file_name):
        new_data =  {
                    "eventtype": eventtype,
                    "member_id": member_id,
                    "emoji": emoji,
                    "timestamp": time
                    }
        with open(file_name, 'r', encoding = 'utf-8') as f: 
            data = json.load(f)
    
                   
        data["reactions"].append(new_data) #adding the new data in the already existing data
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent = 1)
            f.close()
            #f.seek(0)
        
    else: #json file isnt created yet so the bot creates a file.
        with open(file_name, 'a', encoding = 'utf-8') as f: #creating file
            data = { #new data for the json-file
                "reactions": [
                    {
                        "eventtype": eventtype,
                        "member_id": member_id,
                        "emoji": emoji,
                        "timestamp": time
                    }
                ]
            }
            json.dump(data, f, indent=1) #writing data into json-file
            f.close()

async def new_unreaction_4_log(payload, bot):
    #channel_id = payload.channel_id
    #channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    message_id = payload.message_id
    #message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react 
    server_id = payload.guild_id
    server = bot.get_guild(payload.guild_id) #getting guild
    member_id = payload.user_id #getting member
    member = server.get_member(member_id)
    #reactions = message.reactions
    emoji = payload.emoji.name    
    time = str(datetime.datetime.now(datetime.timezone.utc))
    eventtype = "reaction_removed"
    #v1:
    #file_name = "./Logs/Reactions/V1/" + str(server_id) + "/" + str(message_id) + ".json"
    #if os.path.exists(file_name):
    #    new_data =  {
    #                "eventtype": eventtype,
    #                "member": member_id,
    #                "member_name": member.name,
    #                "emoji": emoji,
    #                "timestamp": time
    #                }
    #    with open(file_name, 'r', encoding = 'utf-8') as f: 
    #        data = json.load(f)                   
    #    data["reactions"].append(new_data) #adding the new data in the already existing data
    #    with open(file_name, 'w', encoding='utf-8') as f:
    #        json.dump(data, f, indent = 1)
    #        f.close()
            #f.seek(0)
        
    #else: #json file isnt created yet so the bot creates a file.
    #    with open(file_name, 'a', encoding = 'utf-8') as f: #creating file
    #        data = { #new data for the json-file
    #            "reactions": [
    #                {
    #                    "eventtype": eventtype,
    #                    "member": member_id,
    #                    "member_name": member.name,
    #                    "emoji": emoji,
    #                    "timestamp": time
    #                }
    #            ]
    #        }
    #        json.dump(data, f, indent=1) #writing data into json-file
    #        f.close()

def write_into_log(eventtype, memberid, guildid, channelid, messageid, reaction, timestamp):
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name) #connect to polldatabase
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messagelog VALUES (?, ?, ?, ?, ?, ?, ?)", (eventtype, memberid, guildid, channelid, messageid, reaction, timestamp)) #write into the table the data
    connection.commit()
    connection.close()