import asqlite

async def get_autoroles(bot, guildid, membergroup):
    roleidsmembergroupusers = await asqlite_pull_all_data(bot=bot, statement=f'SELECT roleid FROM autorole WHERE guildid = {guildid} AND membergroup = {membergroup}', data_to_return="roleid")
    return(roleidsmembergroupusers)

async def change_xp_by(bot, guildid, memberid, xptomodify):
    xp = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND memberid = {memberid}", data_to_return="xp")
    await asqlite_update_data(bot=bot, statement=f"UPDATE membertable set xp = {xp + xptomodify} WHERE guildid = {guildid} AND memberid = {memberid}")
    return(xp)

async def get_logchannelid(bot, guildid):
    logchannelid = await asqlite_pull_data(bot=bot, statement=f'SELECT * FROM guildsetup WHERE guildid = {guildid}', data_to_return="logchannelid")
    return(logchannelid)

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
        datarow = await datacursor.fetchall()
        if datarow is None:
            data = None
        else:
            data = datarow[data_to_return]
    return(data)

async def asqlite_update_data(bot, statement):
    async with bot.pool.acquire() as connection:
        await connection.execute(statement)
        await connection.commit()
        
async def asqlite_insert_data(bot, statement):
    async with bot.pool.acquire() as connection:
        await connection.execute(statement)
        await connection.commit()

async def asqlite_get_counter(bot, statement):
    async with bot.pool.acquire() as connection:
        counter = await connection.execute(statement)
        return(counter)