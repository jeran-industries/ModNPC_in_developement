import discord
import aiosqlite

async def add_autorole_2_user(member):
    roles = []
    guild = member.guild
    guildid = guild.id
    connection = await aiosqlite.connect("./database/database.db")

    print("\n Im here \n")

    #all(0) usergroups: bot(1) and humanusers(2)
    membergroup = 0
    roleidsalluserscursor = await connection.execute('SELECT roleid FROM autorole WHERE guildid = ? AND membergroup = ?', (guildid, membergroup))
    roleidsallusers = await roleidsalluserscursor.fetchall()
    await roleidsalluserscursor.close()
    roles = await getroles(roles=roles, roleids=roleidsallusers, guild=guild, member=member)

    #botusers:
    if member.bot == True:
        membergroup=1
        roleidsbotuserscursor = await connection.execute('SELECT roleid FROM autorole WHERE guildid = ? AND membergroup = ?', (guildid, membergroup))
        roleidsallbotusers = await roleidsbotuserscursor.fetchall()
        await roleidsbotuserscursor.close()
        if roleidsallbotusers != []:
            roles = await getroles(roles=roles, roleids=roleidsallbotusers, guild=guild, member=member)

    #humanusers:
    else:
        membergroup=2
        roleidshumanuserscursor = await connection.execute('SELECT roleid FROM autorole WHERE guildid = ? AND membergroup = ?', (guildid, membergroup))
        roleidsallhumanusers = await roleidshumanuserscursor.fetchall()
        await roleidshumanuserscursor.close()
        if roleidsallbotusers != []:
            roles = await getroles(roles=roles, roleids=roleidsallhumanusers, guild=guild, member=member)

    await connection.close()

async def getroles(roles, roleids, guild, member):
    for roleid in roleids:
        roleid = roleid[0]
        if roleid is None:
            if roles == []:
                roles = None
            return(roles)
        elif roleid == []:
            pass
        else:
            role = guild.get_role(roleid)
            if role.is_assignable():
                roles.append(role)
                await member.add_roles(role)

    if roles == []:
        roles = None
    return(roles)