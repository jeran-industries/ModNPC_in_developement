import asqlite

#anounymous messages:


#autoroles:
async def get_autorole(bot, membergroup, roleid):
    roleid = await asqlite_pull_data(bot=bot, statement=f'SELECT * FROM autorole WHERE roleid = {roleid} AND membergroup = {membergroup}', data_to_return="roleid")
    return(roleid)

async def get_autoroles(bot, guildid, membergroup):
    roleidsmembergroupusers = await asqlite_pull_all_data(bot=bot, statement=f'SELECT roleid FROM autorole WHERE guildid = {guildid} AND membergroup = {membergroup}', data_to_return="roleid")
    return(roleidsmembergroupusers)

async def update_autorole_2_other_membergroup(bot, membergroup, roleid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE autorole set membergroup = {membergroup} WHERE roleid = {roleid}")

async def insert_autorole(bot, guildid, roleid, membergroup):
    await asqlite_insert_data(bot=bot, statement=f"INSERT INTO autorole VALUES ({guild_id}, {roleid}, {membergroup})")

async def delete_all_autoroles(bot, guildid):
    await asqlite_delete(bot=bot, statement=f"DELETE FROM autorole WHERE guildid = {guildid}")

#levelsystem:
async def change_xp_by(bot, guildid, memberid, xptomodify, xptoset = None):
    if xptoset is not None:
        newxp = xptoset
    else:
        xp = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND memberid = {memberid}", data_to_return="xp")
        if xp==None:
            xp=0
        newxp = xp + xptomodify
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set xp = {newxp} WHERE guildid = {guildid} AND memberid = {memberid}")
    return(newxp)

async def update_voicetime(bot, guildid, memberid, voicetimetomodify = None):
    if voicetimetomodify is not None:
        voicetime = voicetimetomodify-1
    else:
        voicetime = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND memberid = {memberid}", data_to_return="voicetime")
        if voicetime==None:
            voicetime=0
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set voicetime = {voicetime + 1} WHERE guildid = {guildid} AND memberid = {memberid}")

async def update_messagecounter(bot, guildid, memberid, messagecountertomodify = None):
    if messagecountertomodify is not None:
        messagessent = messagecountertomodify-1
    else:
        messagessent = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND memberid = {memberid}", data_to_return="messagessent")
        if messagessent is None:
            messagessent = 0
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set messagessent = {messagessent + 1} WHERE guildid = {guildid} AND memberid = {memberid}")

async def reset_memberstats(bot, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set messagessent = 0 WHERE guildid = {guildid}")
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set voicetime = 0 WHERE guildid = {guildid}")
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set xp = 0 WHERE guildid = {guildid}")

async def get_lastupvote(bot, guildid, memberid):
    lastupvote = await asqlite_pull_data(bot=bot, statement=f'SELECT last_upvote FROM membertable WHERE guildid = {guildid} AND memberid = {memberid}', data_to_return="last_upvote")
    return(lastupvote)

async def update_lastupvote(bot, time, guildid, memberid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set last_upvote = {time} WHERE guildid = {guildid} AND memberid = {memberid}")

async def activate_levelsystem(bot, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set levelingsystemstatus = 1 WHERE guildid = {guildid}")

async def deactivate_levelsystem(bot, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set levelingsystemstatus = 0 WHERE guildid = {guildid}")

async def update_levelingpingchannel(bot, channelid, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set levelingpingmessagechannel = {channelid} WHERE guildid = {guildid}")

async def get_levelrole(bot, roleid):
    roleid=await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM levelroles WHERE roleid = {roleid}", data_to_return="roleid")
    if roleid is None:
        return(False)
    else:
        return(True)

async def get_all_levelroleids(bot, guildid):
    #levelroleids = cursor.execute("SELECT roleid FROM levelroles WHERE guildid = ?", (interaction.guild.id, )).fetchall()
    roleids=await asqlite_pull_all_data(bot=bot, statement=f"SELECT * FROM levelroles WHERE guildid = {guildid}", data_to_return="roleid")
    return(roleids)

async def check4levelroles(bot, guildid):
    roleid=await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM levelroles WHERE guildid = {guildid}", data_to_return="roleid")
    if roleid is None:
        return(False)
    else:
        return(True)

async def create_levelrole(bot, guildid, roleid, level, keeprole):
    #cursor.execute(f"INSERT INTO levelroles VALUES ({interaction.guild.id}, {self.role[0].id}, {self.level}, {self.keeprole})") #write into the table the data
    await asqlite_insert_data(bot=bot, statement=f"INSERT INTO levelroles VALUES ({guildid}, {roleid}, {level}, {keeprole})")

async def delete_levelrole(bot, roleid):
    #cursor.execute("DELETE FROM levelroles WHERE roleid = ?", (self.values[0],))
    await asqlite_delete(bot=bot, statement=f"DELETE FROM levelroles WHERE roleid = {roleid}")

#logging:
async def get_logchannelid(bot, guildid):
    logchannelid = await asqlite_pull_data(bot=bot, statement=f'SELECT * FROM guildsetup WHERE guildid = {guildid}', data_to_return="logchannelid")
    return(logchannelid)

async def update_logchannelid(bot, logchannelid, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set logchannelid = {logchannelid} WHERE guildid = {guildid}")

#selfroles:
async def insert_into_selfroles(bot, guildid, messageid, dropdown, color):
    await asqlite_insert_data(bot=bot, statement=f"INSERT INTO selfrolesdata VALUES ({guildid}, {messageid}, {dropdown}, '{color}')")

async def check_4_selfrole(bot, messageid):
    data = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM selfroleoptions WHERE messageid = {messageid}", data_to_return="messageid")
    if data is not None:
        return(True)
    else:
        return(False)

async def insert_into_selfrole_options(bot, messageid, emoji, roleid, description):
    await asqlite_insert_data(bot=bot, statement=f"INSERT INTO selfroleoptions VALUES ({messageid}, '{emoji}', {roleid}, '{description}')")

async def get_selfrole_roleid(bot, messageid, emoji):
    try:
        roleid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM selfroleoptions WHERE messageid = {messageid} AND emoji = '{emoji}'", data_to_return="roleid")
    except:
        roleid = None
    return(roleid)

#welcomemessages:
async def insert_into_welcomemessage(bot, guildid, channelid, headerwelcomemessage, contentwelcomemessage):
    #"INSERT INTO welcomemessagetable VALUES (?, ?, ?, ?)", (interaction.guild.id, channelid, headerwelcomemessage, contentwelcomemessage)
    await asqlite_insert_data(bot=bot, statement=f"INSERT INTO welcomemessagetable VALUES ({guildid}, {channelid}, {headerwelcomemessage}, {contentwelcomemessage})")

#guildmanagement:
async def check_4_guild(bot, guildid):
    data = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM guildsetup WHERE guildid = {guildid}", data_to_return="guildid")
    if data is not None:
        return(True)
    else:
        return(False)

async def insert_into_guildtable(bot, guildid):
    
    levelingsystemstatus=False
    levelingpingmessagechannel=None
    welcomemessagestatus=False
    anonymousmessagecooldown=None
    anonymousmessagestatus=False
    botupdatestatus=False
    botupdatechannelid=None
    logchannelid=None
    await asqlite_insert_data(bot=bot, statement=f"INSERT INTO guildsetup VALUES ({guildid}, '{levelingsystemstatus}', '{levelingpingmessagechannel}', '{welcomemessagestatus}', '{anonymousmessagecooldown}', '{anonymousmessagestatus}', '{botupdatestatus}', '{botupdatechannelid}', '{logchannelid}')")

#creating tables:
async def create_guildsetup_table(bot):
    #botupdatestatus BOOL, botupdatechannelid INTEGER)"
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS guildsetup (guildid INTEGER, levelingsystemstatus BOOL, levelingpingmessagechannel INTEGER, welcomemessagestatus BOOL, anonymousmessagecooldown INTEGER, anonymousmessagestatus BOOL, botupdatestatus BOOL, botupdatechannelid INTEGER, logchannelid INTEGER)")

async def create_autorole_table(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS autorole (guildid INTEGER, roleid INTEGER, membergroup INTEGER)")

async def create_levelroles_table(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS levelroles (guildid INTEGER, roleid INTEGER, level INTEGER, keeprole BOOL)")

async def create_member_table(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS membertable (guildid INTEGER, memberid INTEGER, messagessent INTEGER, voicetime INTEGER, xp INTEGER, status TEXT, joinedintosystem TEXT, last_upvote INTEGER)")

#functions to connect to db with asqlite
async def asqlite_pull_data(bot, statement, data_to_return):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute(statement)
        datarow = await datacursor.fetchone()
        if datarow is None:
            data = None
        else:
            data = datarow[data_to_return]
    return(data)

async def asqlite_pull_all_data(bot, statement, data_to_return):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute(statement)
        datarows = await datacursor.fetchall()
        if datarows is None:
            data = None
        else:
            data = []
            for datarow in datarows:
                data.append(datarow[data_to_return])
    return(data)

async def asqlite_update_data(bot, statement):
    async with bot.pool.acquire() as connection:
        await connection.execute(statement)
        await connection.commit()
        
async def asqlite_insert_data(bot, statement):
    async with bot.pool.acquire() as connection:
        await connection.execute(statement)
        await connection.commit()

async def asqlite_create_table(bot, statement):
    async with bot.pool.acquire() as connection:
        await connection.execute(statement)
        await connection.commit()

async def asqlite_get_counter(bot, statement):
    async with bot.pool.acquire() as connection:
        counter = await connection.execute(statement)
        return(counter)

async def asqlite_delete(bot, statement):
    async with bot.pool.acquire() as connection:
        await connection.execute(statement)
        await connection.commit()