import os
import json
import datetime
import discord
import sqlite3

#own modules:
#from levelsystem import leaderboardnewmember

def new_member(member): #new member -> new jsonfile with member_id
    #v1:
    #if isinstance(member, member) == True:
    #    #recdleaderboardnewmember(member.id)
    #    file_name = "./Member/" + str(member.guild.id) + "/" + str(member.id) + ".json"
    #    with open(file_name, 'a+', encoding='utf-8') as f: #opening the right file with utf-8 as encoding
    #        data =  {"stats":
    #                    [
    #                        {
    #                        "membername": member.name,
    #                        "messagessent": 0,
    #                        "messagesentonceaminute": 0, #triggered once a minute and send to one bez u cant get xps by spamming
    #                        "voicetime": 0,
    #                        "xp": 0
    #                        }
    #                    ],
    #                "log":
    #                    [
    #                        {
    #                        "timestamp": str(datetime.datetime.now(datetime.timezone.utc)),
    #                        "membereventtype": "joined or entered into leveling system the first time"      
    #                        }
    #                    ]                     
    #                }
    #        json.dump(data, f, indent = 1)
    #        f.close()
    
    #v2:
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name) #connect to polldatabase
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS membertable (guildid INTEGER, memberid INTEGER, messagessent INTEGER, voicetime INTEGER, xp INTEGER, status TEXT, joinedintosystem TEXT)") #creates a table
    try:
        if (cursor.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (member.guild.id, member.id)).fetchone()) is None:
            cursor.execute("INSERT INTO membertable VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (member.guild.id, member.id, 0, 0, 0, "Joined", str(datetime.datetime.now(datetime.timezone.utc)), 0, 0)) #write into the table the data
    except AttributeError:
        pass
    if (cursor.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (0, member.id)).fetchone()) is None:
        cursor.execute("INSERT INTO membertable VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (0 , member.id, 0, 0, 0, "Joined", str(datetime.datetime.now(datetime.timezone.utc)), 0)) #write into the table the data
    cursor.execute("CREATE TABLE IF NOT EXISTS memberlog (guildid INTEGER, memberid INTEGER, timestamp TEXT, status TEXT)")
    if isinstance(member, discord.Member):
        if (cursor.execute("SELECT * FROM memberlog WHERE guildid = ? AND memberid = ?", (member.guild.id, member.id)).fetchone()) is None:
            cursor.execute("INSERT INTO memberlog VALUES (?, ?, ?, ?)", (member.guild.id, member.id, str(datetime.datetime.now(datetime.timezone.utc)), "Joined or entered first time the system")) #write into the table the data
    connection.commit()
    connection.close()
