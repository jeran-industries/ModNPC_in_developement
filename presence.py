import discord
import sqlite3

async def presenceupdate(bot):
    connection = sqlite3.connect("./database/database.db") #connect to polldatabase
    cursor = connection.cursor()
    guildcounter = len(cursor.execute("SELECT * FROM guildsetup").fetchall())
    membercounter = len(cursor.execute("SELECT * FROM membertable WHERE guildid = ? AND status = ?", (0, "Joined")).fetchall())
    connection.close()
    await bot.change_presence(status=discord.Status.online, activity = discord.Game(f"Watching {guildcounter} servers with {membercounter} members"))