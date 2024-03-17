import os
import json
import sqlite3

def messagesenteventlog(message):
    eventtype = "sent"
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
    write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.created_at))

def messageeditedeventlog(message):
    eventtype = "edited"
    #v2:
    write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.edited_at))

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

    file_name_of_selfrole = "./Selfroles/V1/" + str(message.guild.id) + '/' + str(message.channel.id) + ".json"
    if file_name_of_selfrole.exists:
        os.remove(file_name_of_selfrole)
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