from datetime import datetime
import asqlite

#own modules:
#from levelsystem import leaderboardnewmember
#from autoroles import add_autorole_2_user
from sqlitehandler import asqlite_insert_data, asqlite_pull_data, asqlite_update_data

async def new_member(member, bot): #new member -> new jsonfile with member_id
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
    #async with asqlite.Pool.acquire(bot.pool) as connection:
    #    await connection.execute("INSERT INTO membertable VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (member.guild.id, member.id, 0, 0, 0, "Joined", str(datetime.datetime.now(datetime.timezone.utc)), 0)) #write into the table the data
    #    await connection.execute("INSERT INTO membertable VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (0 , member.id, 0, 0, 0, "Joined", str(datetime.datetime.now(datetime.timezone.utc)), 0)) #write into the table the data
    #    await connection.commit()
    time = int(round((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
    if await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {member.guild.id} AND memberid = {member.id}", data_to_return="memberid") is None:
        status = "Joined"
        await asqlite_insert_data(bot=bot, statement=f"INSERT INTO membertable VALUES ({member.guild.id}, {member.id}, {0}, {0}, {0}, {0}, {time}, {0})")