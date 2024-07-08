import asqlite

#anounymous messages:


#autoroles:
async def get_autorole(bot, membergroup, roleid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM autorole WHERE roleid = ? AND membergroup = ?", (roleid, membergroup))
        datarow = await datacursor.fetchone()
        return(datarow["roleid"])

async def get_autoroles(bot, guildid, membergroup):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT roleid FROM autorole WHERE guildid = ? AND membergroup = ?", (guildid, membergroup))
        datarows = await datacursor.fetchall()
        return(datarows)

async def update_autorole_2_other_membergroup(bot, membergroup, roleid):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE autorole SET membergroup = ? WHERE roleid = ?", (membergroup, roleid))
        await connection.commit()

async def insert_autorole(bot, guildid, roleid, membergroup):
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO autorole VALUES (?, ?, ?)", (guildid, roleid, membergroup))
        await connection.commit()

async def delete_all_autoroles(bot, guildid):
    async with bot.pool.acquire() as connection:
        await connection.execute("DELETE FROM autorole WHERE guildid = ?", (guildid))
        await connection.commit()

#custom voicechats:
async def check4cvcstatus(bot, guildid):
    async with bot.pool.acquire() as connection:
        print(guildid)
        datacursor = await connection.execute("SELECT * FROM guildsetup WHERE guildid = ?", (guildid))
        datarow = await datacursor.fetchone()
        cvcstatus = datarow["cvcstatus"]
        print(cvcstatus)
        if cvcstatus is None or cvcstatus == 0:
            return(False)
        return(cvcstatus)

async def check4jointocreatechannel(bot, guildid, channelid):
    cvcstatus = await check4cvcstatus(bot=bot, guildid=guildid)
    if cvcstatus != 1:
        return(False)

    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM guildsetup WHERE guildid = ?", (guildid))
        datarow = await datacursor.fetchone()
        join2channelid = datarow["jointocreatechannelid"]
        print(join2channelid)
        if join2channelid == channelid:
            return(True)
        else:
            return(False)

async def check4savedcvc(bot, guildid, ownerid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM cvctable WHERE guildid = ? AND ownerid = ?", (guildid, ownerid))
        datarow = await datacursor.fetchone()
        if datarow is None:
            print(f"There is nothing")
            return(False)
        #elif datarow["guildid"] is True:
        #    print(f"This is {datarow["guildid"]}")
        #    return(True)
        else:
            #print(f"This is {datarow["guildid"]}.")
            return(True)

async def check4currentcvc(bot, guildid, ownerid, channelid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM currentcvctable WHERE channelid = ?", (channelid))
        datarow = await datacursor.fetchone()
        if datarow is None:
            print(f"There is nothing")
            return(False)
        #elif datarow["guildid"] is True:
        #    print(f"This is {datarow["guildid"]}")
        #    return(True)
        else:
            #print(f"This is {datarow["guildid"]}.")
            return(True)

async def insert_cvc(bot, guildid, ownerid, name):
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO cvctable VALUES (?, ?, ?, ?, ?, ?)", (guildid, ownerid, f"CVC from {name}", 0, 0, None))
        await connection.commit()

async def update_cvc(bot, guildid, ownerid, name, status, vclimit, password):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE cvctable SET name = ?, status = ?, vclimit = ?, password = ? WHERE guildid = ? AND ownerid = ?", (name, status, vclimit, password, guildid, ownerid))
        await connection.commit()

async def get_cvc(bot, guildid, ownerid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM cvctable WHERE guildid = ? AND ownerid = ?", (guildid, ownerid))
        datarow = await datacursor.fetchone()
        name = datarow["name"]
        status = datarow["status"]
        vclimit = datarow["vclimit"]
        password = datarow["password"]
        return(name, status, vclimit, password)

async def get_current_cvc(bot, channelid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM currentcvctable WHERE channelid = ?", (channelid))
        datarow = await datacursor.fetchone()
        if datarow is not None:
            ownerid = datarow["ownerid"]
            name = datarow["name"]
            status = datarow["status"]
            vclimit = datarow["vclimit"]
            password = datarow["password"]
            return(ownerid, name, status, vclimit, password)
        else:
            return(None, None, None, None, None)

async def get_current_cvc_by_ownerid(bot, guildid, ownerid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM currentcvctable WHERE guildid = ? AND ownerid = ?", (guildid, ownerid))
        datarow = await datacursor.fetchone()
        if datarow is not None:
            ownerid = datarow["ownerid"]
            name = datarow["name"]
            status = datarow["status"]
            vclimit = datarow["vclimit"]
            password = datarow["password"]
            return(ownerid, name, status, vclimit, password)
        else:
            return(None, None, None, None, None)

async def get_current_cvcs(bot):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM currentcvctable")
        datarows = await datacursor.fetchall()
        channelids = []
        for datarow in datarows:
            channelids.append(datarow["channelid"])
            print(channelids)
        return(channelids)

async def get_permitted_member(bot, guildid, ownerid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM cvcpermittedpeopletable WHERE guildid = ? AND ownerid = ?", (guildid, ownerid))
        datarows = await datacursor.fetchall()
        print(datarows)
        members = []
        for datarow in datarows:
            members.append(datarow["memberid"])
            print(members)
        return(members)

async def get_current_permitted_member(bot, channelid, ownerid=None):
    async with bot.pool.acquire() as connection:
        if ownerid is None:
            datacursor = await connection.execute("SELECT * FROM currentcvcpermittedpeopletable WHERE channelid = ?", (channelid))
        else:
            datacursor = await connection.execute("SELECT * FROM currentcvcpermittedpeopletable WHERE channelid = ? AND ownerid = ?", (channelid, ownerid))
        datarows = await datacursor.fetchall()
        print(datarows)
        members = []
        for datarow in datarows:
            members.append(datarow["memberid"])
            print(members)
        return(members)

async def get_cvc_where_member_blocked(bot, guildid, memberid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM cvcbannedpeopletable WHERE guildid = ? AND memberid = ?", (guildid, memberid))
        datarows = await datacursor.fetchall()
        print(datarows)
        ownerids = []
        for datarow in datarows:
            ownerids.append(datarow["ownerids"])
            print(ownerids)
        return(ownerids)

async def get_blocked_member(bot, guildid, ownerid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM cvcbannedpeopletable WHERE guildid = ? AND ownerid = ?", (guildid, ownerid))
        datarows = await datacursor.fetchall()
        print(datarows)
        members = []
        for datarow in datarows:
            members.append(datarow["memberid"])
            print(members)
        return(members)

async def get_mods(bot, guildid, ownerid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM cvcmodstable WHERE guildid = ? AND ownerid = ?", (guildid, ownerid))
        datarows = await datacursor.fetchall()
        print(datarows)
        members = []
        for datarow in datarows:
            members.append(datarow["memberid"])
            print(members)
        return(members)

async def insert_into_current_cvctable(bot, guildid, ownerid, channelid, name, status, vclimit, password):
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO currentcvctable VALUES (?, ?, ?, ?, ?, ?, ?)", (guildid, ownerid, channelid, name, status, vclimit, password))
        await connection.commit()

async def add_current_permitted_user(bot, guildid, ownerid, channelid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO currentcvcpermittedpeopletable VALUES (?, ?, ?, ?)", (guildid, ownerid, channelid, memberid))
        await connection.commit()

async def delete_current_permitted_user(bot, channelid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("DELETE FROM currentcvcpermittedpeopletable WHERE channelid = ? AND memberid = ?", (channelid, memberid))
        await connection.commit()

async def add_permitted_user(bot, guildid, ownerid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO cvcpermittedpeopletable VALUES (?, ?, ?)", (guildid, ownerid, memberid))
        await connection.commit()

async def remove_permitted_user(bot, guildid, ownerid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("DELETE FROM cvcpermittedpeopletable WHERE guildid = ? AND ownerid = ? AND memberid = ?", (guildid, ownerid, memberid))
        await connection.commit()

async def change_customvc_status(bot, status, guildid, channelid = None):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE guildsetup set cvcstatus = ? WHERE guildid = ?", (status, guildid))
        if status is True and channelid is not None:
            await connection.execute("UPDATE guildsetup set jointocreatechannelid = ? WHERE guildid = ?", (channelid, guildid))
        await connection.commit()

async def change_ownerid(bot, channelid, ownerid):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE currentcvctable set ownerid = ? WHERE channelid = ?", (ownerid, channelid))
        await connection.commit()

async def add_mod(bot, guildid, ownerid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO cvcmodstable VALUES (?, ?, ?)", (guildid, ownerid, memberid))
        await connection.commit()

async def remove_mod(bot, guildid, ownerid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("DELETE FROM cvcmodstable WHERE guildid = ? AND ownerid = ? AND memberid = ?", (guildid, ownerid, memberid))
        await connection.commit()

async def rename_current_cvc(bot, channelid, name):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE currentcvctable set name = ? WHERE channelid = ?", (name, channelid))
        await connection.commit()

async def limit_current_cvc(bot, channelid, vclimit):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE currentcvctable set vclimit = ? WHERE channelid = ?", (vclimit, channelid))
        await connection.commit()
    
async def delete_current_cvc(bot, channelid):
    #await statement=f"DELETE FROM levelroles WHERE roleid = {roleid}")
    async with bot.pool.acquire() as connection:
        await connection.execute("DELETE FROM currentcvctable WHERE channelid = ?", (channelid))
        await connection.commit()

async def delete_current_permits(bot, channelid):
    async with bot.pool.acquire() as connection:
        await connection.execute("DELETE FROM currentcvcpermittedpeopletable WHERE channelid = ?", (channelid))
        await connection.commit()

async def add_blocked_person(bot, guildid, ownerid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO cvcbannedpeopletable VALUES (?, ?, ?)", (guildid, ownerid, memberid))
        await connection.commit()

async def remove_blocked_person(bot, guildid, ownerid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("DELETE FROM cvcbannedpeopletable WHERE guildid = ? AND ownerid = ? AND memberid = ?", (guildid, ownerid, memberid))
        await connection.commit()

#levelsystem:
#async def change_xp(bot, guildid, memberid, xptoset):
#    pass

async def change_xp_by(bot, guildid, memberid, xptomodify, xptoset = None):
    if xptoset is not None:
        newxp = xptoset
    else:
        async with bot.pool.acquire() as connection:
            datacursor = await connection.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, memberid))
            datarow = await datacursor.fetchone()
        if datarow is None:
            xp=0
        else:
            xp = datarow["xp"]
        newxp = xp + xptomodify
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE membertable SET xp = ? WHERE guildid = ? AND memberid = ?", (newxp, guildid, memberid))
        await connection.commit()
    return(newxp)

async def update_voicetime(bot, guildid, memberid, voicetimetomodify = None):
    if voicetimetomodify is not None:
        voicetime = voicetimetomodify-1
    else:
        async with bot.pool.acquire() as connection:
            datacursor = await connection.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, memberid))
            datarow = await datacursor.fetchone()
        if datarow is None:
            voicetime=0
        else:
            voicetime = datarow["voicetime"]
    async with bot.pool.acquire() as connection:
        voicetime = voicetime + 1
        await connection.execute("UPDATE membertable SET voicetime = ? WHERE guildid = ? AND memberid = ?", (voicetime, guildid, memberid))
        await connection.commit()

async def update_messagecounter(bot, guildid, memberid, messagecountertomodify = None):
    messagessent = 0
    if messagecountertomodify is not None:
        messagessent = messagecountertomodify-1
    else:
        async with bot.pool.acquire() as connection:
            datacursor = await connection.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, memberid))
            datarow = await datacursor.fetchone()
            if datarow is not None:
                messagessent = datarow["messagessent"]
    async with bot.pool.acquire() as connection:
        messagessent = messagessent + 1
        await connection.execute("UPDATE membertable SET messagessent = ? WHERE guildid = ? AND memberid = ?", (messagessent, guildid, memberid))
        await connection.commit()

async def reset_memberstats(bot, guildid):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE membertable SET messagessent = ? WHERE guildid = ?", (0, guildid))
        await connection.execute("UPDATE membertable SET voicetime = ? WHERE guildid = ?", (0, guildid))
        await connection.execute("UPDATE membertable SET xp = ? WHERE guildid = ?", (0, guildid))
        await connection.commit()

async def get_lastupvote(bot, guildid, memberid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, memberid))
        datarow = await datacursor.fetchone()
        return(datarow["last_upvote"])

async def update_lastupvote(bot, time, guildid, memberid):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE membertable SET last_upvote = ? WHERE guildid = ? AND memberid = ?", (time, guildid, memberid))
        await connection.commit()

async def activate_levelsystem(bot, guildid):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE guildsetup SET levelingsystemstatus = 1 WHERE guildid = ?", (guildid))
        await connection.commit()

async def deactivate_levelsystem(bot, guildid):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE guildsetup SET levelingsystemstatus = 0 WHERE guildid = ?", (guildid))
        await connection.commit()

async def update_levelingpingchannel(bot, channelid, guildid):
    async with bot.pool.acquire() as connection:
        await connection.execute("UPDATE guildsetup SET levelingpingmessagechannel = ? WHERE guildid = ?", (channelid, guildid))
        await connection.commit()

async def get_levelrole(bot, roleid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM levelroles WHERE roleid = ?", (roleid))
        datarow = await datacursor.fetchone()
        roleid = datarow["roleid"]
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

async def get_logwebhookid(bot, guildid):
    logwebhookid = await asqlite_pull_data(bot=bot, statement=f'SELECT * FROM guildsetup WHERE guildid = {guildid}', data_to_return="logwebhookid")
    return(logwebhookid)

async def update_logwebhookid(bot, logwebhookid, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set logwebhookid = {logwebhookid} WHERE guildid = {guildid}")

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

#ticketsystem:
async def activate_ticketsystem(bot, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set ticketsystemstatus = '{True}' WHERE guildid = {guildid}")

async def deactivate_ticketsystem(bot, guildid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set ticketsystemstatus = '{False}' WHERE guildid = {guildid}")

async def update_channel_ticketsystem(bot, guildid, channelid):
    if channelid is None:
        await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set ticketsystemchannelid = 'None' WHERE guildid = {guildid}")
    else:
        await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set ticketsystemchannelid = {channelid} WHERE guildid = {guildid}")

async def update_opentickets_category_ticketsystem(bot, guildid, categoryid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set ticketsystemopencategoryid = {categoryid} WHERE guildid = {guildid}")

async def update_closedtickets_category_ticketsystem(bot, guildid, categoryid):
    await asqlite_update_data(bot=bot, statement=f"UPDATE guildsetup set ticketsystemclosedcategoryid = {categoryid} WHERE guildid = {guildid}")

async def get_opentickets_categoryid(bot, guildid):
    opentickets_categoryid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM guildsetup WHERE guildid = {guildid}", data_to_return="ticketsystemopencategoryid")
    return(opentickets_categoryid)

async def get_closedtickets_categoryid(bot, guildid):
    closedtickets_categoryid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM guildsetup WHERE guildid = {guildid}", data_to_return="ticketsystemclosedcategoryid")
    return(closedtickets_categoryid)

async def get_ticketsystem_status(bot, guildid):
    ticketsystemstatus = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM guildsetup WHERE guildid = {guildid}", data_to_return="ticketsystemstatus")
    return(ticketsystemstatus)

async def insert_into_tickettable(bot, guildid, channelid, creatorid):
    #ticketsystemtable (guildid INTEGER, ticketid INTEGER, ticketstatus INTEGER, creatorid INTEGER, claimerid INTEGER
    await asqlite_insert_data(bot=bot, statement=f"INSERT INTO ticketsystemtable VALUES ({guildid}, {channelid}, {0}, {creatorid}, {0})")

async def update_ticket_status(bot, ticketid, status, claimerid = None):
    await asqlite_update_data(bot=bot, statement=f"UPDATE ticketsystemtable set ticketstatus = {status} WHERE ticketid = {ticketid}")
    if claimerid is not None:
        await asqlite_update_data(bot=bot, statement=f"UPDATE ticketsystemtable set claimerid = {claimerid} WHERE ticketid = {ticketid}")

async def get_creatorid_ticket(bot, ticketid):
    creatorid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM ticketsystemtable WHERE ticketid = {ticketid}", data_to_return="creatorid")
    return(creatorid)

async def get_claimerid_ticket(bot, ticketid):
    claimerid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM ticketsystemtable WHERE ticketid = {ticketid}", data_to_return="claimerid")
    return(claimerid)

#async def ticketsystempermissions(bot, memberid = None, roleid = None):


#welcomemessages:
async def insert_into_welcomemessage(bot, guildid, channelid, headerwelcomemessage, contentwelcomemessage):
    #"INSERT INTO welcomemessagetable VALUES (?, ?, ?, ?)", (interaction.guild.id, channelid, headerwelcomemessage, contentwelcomemessage)
    #print(headerwelcomemessage)
    #print(contentwelcomemessage)
    #conn.execute("INSERT INTO Employees (ID,NAME,AGE,ADDRESS,SALARY) \  VALUES (1, 'Ajeet', 27, 'Delhi', 20000.00 )");  
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO welcomemessagetable VALUES (?, ?, ?, ?, ?)", (guildid, channelid, headerwelcomemessage, contentwelcomemessage, True))
        await connection.commit()

async def check_4_welcomemessage(bot, guildid):
    data = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM welcomemessagetable WHERE guildid = {guildid}", data_to_return="guildid")
    if data is not None:
        return(True)
    else:
        return(False)

async def delete_welcomemessage(bot, guildid):
    await asqlite_delete(bot=bot, statement=f"DELETE FROM welcomemessagetable WHERE guildid = {guildid}")

#membermanagement:
async def check4member(bot, guildid, memberid):
    async with bot.pool.acquire() as connection:
        datacursor = await connection.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, memberid))
        datarow = await datacursor.fetchone()
        if datarow is None:
            return(False)
        else:
            return(True)

async def insert_new_member(bot, guildid, memberid, time, status):
    async with bot.pool.acquire() as connection:
        #guildid, memberid, messagessent, voicetime, xp, status, time when joined, last upvote
        await connection.execute("INSERT INTO membertable VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (guildid, memberid, 0, 0, 0, status, time, 0))
        await connection.commit()

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
    ticketsystemstatus=False
    ticketsystemchannel=None
    ticketsystemopencategoryid=None
    ticketsystemclosedcategoryid=None
    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO guildsetup VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (guildid, levelingsystemstatus, levelingpingmessagechannel, welcomemessagestatus, anonymousmessagecooldown, anonymousmessagestatus, botupdatestatus, botupdatechannelid, logchannelid, ticketsystemstatus, ticketsystemchannel, ticketsystemopencategoryid, ticketsystemclosedcategoryid, None, None, None))
        await connection.commit()
    #await asqlite_insert_data(bot=bot, statement=f"INSERT INTO guildsetup VALUES ({guildid}, '{levelingsystemstatus}', '{levelingpingmessagechannel}', '{welcomemessagestatus}', '{anonymousmessagecooldown}', '{anonymousmessagestatus}', '{botupdatestatus}', '{botupdatechannelid}', '{logchannelid}', '{ticketsystemstatus}', '{ticketsystemchannel}', {ticketsystemopencategoryid}, {ticketsystemclosedcategoryid})")

#permissions: permissiontable: roleid INTEGER, memberid INTEGER, permission TEXT, status BOOL

#ticketsystempermissions: ticketprocessor
async def de_activate_permission(bot, guildid, status, permission, roleid = None, memberid = None):
    if roleid is not None:
        permissionstatus=await get_permission_status(bot=bot, permission=permission, roleid=roleid)
        if permissionstatus is not None:
            if permissionstatus != status:
                async with bot.pool.acquire() as connection:
                    await connection.execute("UPDATE permissiontable SET status = ?, WHERE roleid = ? AND permission = ?", (status, roleid, permission))
                    await connection.commit()
                    return(None)
            else:
                return

    elif memberid is not None:
        permissionstatus=await get_permission_status(bot=bot, permission=permission, memberid=memberid)
        if permissionstatus is not None:
            if permissionstatus != status:
                async with bot.pool.acquire() as connection:
                    await connection.execute("UPDATE permissiontable SET status = ?, WHERE memberid = ? AND permission = ?", (status, memberid, permission))
                    await connection.commit()
                    return(None)
            else:
                return

    async with bot.pool.acquire() as connection:
        await connection.execute("INSERT INTO permissiontable VALUES (?, ?, ?, ?, ?)", (guildid, roleid, memberid, permission, status))
        await connection.commit()

async def get_permissions(bot, permission, guildid):
    #if roleid is not None and memberid is not None:
    #    raise(Warning, "Only the roleid will be ")

    async with bot.pool.acquire() as connection:
        roleids = []
        memberids = []
        datacursor = await connection.execute("SELECT * FROM permissiontable WHERE guildid = ? AND permission = ?", (guildid, permission))
        datarows = await datacursor.fetchall()
        for datarow in datarows:
            roleids.append(datarow["roleid"])
            memberids.append(datarow["memberid"])
        if roleids == []:
            roleids = None
        if memberids == []:
            memberids = None
        return(memberids, roleids)

async def get_permission_status(bot, permission, roleid=None, memberid=None):
    #if roleid is not None and memberid is not None:
    #    raise(Warning, "Only the roleid will be ")

    if roleid is not None:
        async with bot.pool.acquire() as connection:
            datacursor = await connection.execute("SELECT * FROM permissiontable WHERE roleid = ? AND permission = ?", (roleid, permission))
            datarow = await datacursor.fetchone()
            if datarow is not None:
                return(datarow["status"])
            else:
                return(None)

    elif memberid is not None:
        async with bot.pool.acquire() as connection:
            datacursor = await connection.execute("SELECT * FROM permissiontable WHERE memberid = ? AND permission = ?", (roleid, permission))
            datarow = await datacursor.fetchone()
            if datarow is not None:
                return(datarow["status"])
            else:
                return(None)

    else:
        return(None)

#creating tables:
async def create_guildsetup_table(bot):
    #botupdatestatus BOOL, botupdatechannelid INTEGER)"
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS guildsetup (guildid INTEGER, levelingsystemstatus BOOL, levelingpingmessagechannel INTEGER, welcomemessagestatus BOOL, anonymousmessagecooldown INTEGER, anonymousmessagestatus BOOL, botupdatestatus BOOL, botupdatechannelid INTEGER, logchannelid INTEGER, logwebhookid INTEGER, ticketsystemstatus BOOL, ticketsystemchannelid INTEGER, ticketsystemopencategoryid INTEGER, ticketsystemclosedcategoryid INTEGER)")

async def create_autorole_table(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS autorole (guildid INTEGER, roleid INTEGER, membergroup INTEGER)")

async def create_levelroles_table(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS levelroles (guildid INTEGER, roleid INTEGER, level INTEGER, keeprole BOOL)")

async def create_member_table(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS membertable (guildid INTEGER, memberid INTEGER, messagessent INTEGER, voicetime INTEGER, xp INTEGER, status TEXT, joinedintosystem TEXT, last_upvote INTEGER)")

async def create_ticketsystemtable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS ticketsystemtable (guildid INTEGER, ticketid INTEGER, ticketstatus INTEGER, creatorid INTEGER, claimerid INTEGER)") #ticketid = messageid ticketstatus = 0(unclaimed) 1(claimed) 2(closed) 3(reopened&unclaimed) 4(reopened&claimed)

    #cursor.execute("CREATE TABLE IF NOT EXISTS welcomemessagetable (guildid INTEGER, channelid INTEGER, header TEXT, content TEXT)")
async def create_welcomemessagetable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS welcomemessagetable (guildid INTEGER, channelid INTEGER, header TEXT, content TEXT, mentionwelcomemessage BOOL)") #ticketid = messageid ticketstatus = 0(unclaimed) 1(claimed) 2(closed) 3(reopened&unclaimed) 4(reopened&claimed)

#cvc
#table cvctable: guildid, ownerid, name, status (locked/unlocked/hided), limit, password
async def create_cvctable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS cvctable (guildid INTEGER, ownerid INTEGER, name TEXT, status INTEGER, vclimit INTEGER, password TEXT)") #status = 0(unlocked) 1(locked) 2(hidden)

#table cvctable: guildid, ownerid, name, status (locked/unlocked/hided), limit, password
async def create_current_cvctable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS currentcvctable (guildid INTEGER, ownerid INTEGER, channelid INTEGER, name TEXT, status INTEGER, vclimit INTEGER, password TEXT)") #status = 0(unlocked) 1(locked) 2(hidden)

#table cvcpermittedpeopletable: guildid, ownerid, memberid
async def create_cvcpermittedpeopletable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS cvcpermittedpeopletable (guildid INTEGER, ownerid INTEGER, memberid INTEGER)") #status = 0(unlocked) 1(locked) 2(hidden)

#table current cvcpermittedpeopletable: guildid, ownerid, memberid
async def create_current_cvcpermittedpeopletable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS currentcvcpermittedpeopletable (guildid INTEGER, ownerid INTEGER, channelid INTEGER, memberid INTEGER)") #status = 0(unlocked) 1(locked) 2(hidden)

#table cvcbannedpeopletable: guildid, ownerid, memberid
async def create_cvcbannedpeopletable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS cvcbannedpeopletable (guildid INTEGER, ownerid INTEGER, memberid INTEGER)") #status = 0(unlocked) 1(locked) 2(hidden)

#table cvcmodstable: guildid, ownerid, memberid
async def create_cvcmodstable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS cvcmodstable (guildid INTEGER, ownerid INTEGER, memberid INTEGER)") #status = 0(unlocked) 1(locked) 2(hidden)

#permissiontable:
async def create_permissiontable(bot):
    await asqlite_create_table(bot=bot, statement="CREATE TABLE IF NOT EXISTS permissiontable (guildid INTEGER, roleid INTEGER, memberid INTEGER, permission TEXT, status BOOL)")

#create indexes:
async def create_unique_index_member_table(bot):
    await asqlite_create_index(bot=bot, statement="CREATE UNIQUE INDEX IF NOT EXISTS membertable_guildid_memberid ON membertable(guildid, memberid)")

#adding columns if needed:
async def add_columns(bot):
    await create_logchannelid_column(bot)
    await create_logwebhookid_column(bot)
    await create_ticketsystemstatus_column(bot)
    await create_ticketsystemchannelid_column(bot)
    await create_ticketsystemopencategoryid_column(bot)
    await create_ticketsystemclosedcategoryid_column(bot)
    await create_mentionwelcomemessage_column(bot)
    await create_cvcstatus_column(bot)
    await create_jointocreatechannel_column(bot)

async def create_logchannelid_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="logchannelid", columntype="INTEGER")

async def create_logwebhookid_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="logwebhookid", columntype="INTEGER")

async def create_ticketsystemstatus_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="ticketsystemstatus", columntype="BOOL")

async def create_ticketsystemchannelid_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="ticketsystemchannelid", columntype="INTEGER")

async def create_ticketsystemopencategoryid_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="ticketsystemopencategoryid", columntype="INTEGER")

async def create_ticketsystemclosedcategoryid_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="ticketsystemclosedcategoryid", columntype="INTEGER")

async def create_mentionwelcomemessage_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="welcomemessagetable", columnname="mentionwelcomemessage", columntype="BOOL")

async def create_cvcstatus_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="cvcstatus", columntype="BOOL")

async def create_jointocreatechannel_column(bot):
    await asqlite_try_2_add_column(bot=bot, table="guildsetup", columnname="jointocreatechannelid", columntype="BOOL")

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

async def asqlite_create_index(bot, statement):
    async with bot.pool.acquire() as connection:
        await connection.execute(statement)
        await connection.commit()

async def asqlite_try_2_add_column(bot, table, columnname, columntype):
    async with bot.pool.acquire() as connection:
        try:
            await connection.execute(f"ALTER TABLE {table} ADD {columnname} {columnname}")
            await connection.commit()
        except:
            pass
    #try:
    #    cursor.execute("ALTER TABLE guildsetup ADD logchannelid INTEGER")
    #except:
    #    pass
    #pass

#unsafe: can run into problem
async def asqlite_add_column(bot, table, columnname, columntype):
    print("DONT USE THIS FUNCTION IN PRODUCTION: CAN RUN INTO PROBLEMS AND RUIN WHOLE STARTUP PROCESS")
    async with bot.pool.acquire() as connection:
        await connection.execute(f"ALTER TABLE {table} ADD {columnname} {columnname}")
        await connection.commit()
