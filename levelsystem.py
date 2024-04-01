import os
import json
import math
import io
import sqlite3
import discord
import aiosqlite
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageShow

#own modules:
from membermanagement import new_member
from link2id import channellink2channelid, channellink2guildid
from checks import check4dm, check4dm_message


async def new_message(bot, message): #make messagecounter bigger in json file bigger
    #v1:
    #file_name = "./Member/" + str(server_id) + "/" + str(member_id) + ".json"
    #file_4_cooldown = "./Member/" + str(server_id) + "/xpcooldowninchat.json"
    #if os.path.exists(file_name):
    #    if message.content[:1] == "/":
    #        return()
    #    with open(file_name, 'r', encoding = 'utf-8') as f:
    #        data = json.load(f)
    #    messagessent = data["stats"][0]["messagessent"]
    #    data["stats"][0]["messagessent"] = messagessent + 1
    #    if data["stats"][0]["messagesentonceaminute"] == 0: #triggered only once a minute so spamming doesnt give xp
    #        #data["stats"][0]["messagesentonceaminute"] = 1
    #        xp = data["stats"][0]["xp"]
    #        data["stats"][0]["xp"] = xp + 1
    #    with open(file_name, 'w', encoding = 'utf-8') as f:
    #        json.dump(data, f, indent = 1)
    #        f.close()
    #else:
        #new_member(member)
        #new_message(message)
    #v2:
    #cursor = connection.cursor()
    try:
        guildid = message.guild.id
    except AttributeError:
        guildid = None
    file_name = "./database/database.db"
    connection = await aiosqlite.connect(file_name) #connect to polldatabase
    await connection.execute("CREATE TABLE IF NOT EXISTS membertable (guildid INTEGER, memberid INTEGER, messagessent INTEGER, voicetime INTEGER, xp INTEGER, status TEXT, joinedintosystem TEXT)") #creates a table
    if guildid is not None:
        messagessentguildcursor = await connection.execute("SELECT messagessent FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, message.author.id))
        messagessentguild = await messagessentguildcursor.fetchone()
        messagessentguild = messagessentguild[0]
        await messagessentguildcursor.close()

        xpguildcursor = await connection.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, message.author.id))
        xpguild = await xpguildcursor.fetchone()
        xpguild = xpguild[0]
        await xpguildcursor.close()

        await connection.execute("UPDATE membertable set messagessent = ? WHERE guildid = ? AND memberid = ?", (messagessentguild + 1, guildid, message.author.id))
        await connection.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpguild + 1, guildid, message.author.id))
        await new_level_ping(bot, message.author.id, guildid, xpguild, xpguild + 1)

    messagessentglobalcursor = await connection.execute("SELECT messagessent FROM membertable WHERE guildid = ? AND memberid = ?", (0, message.author.id))
    messagessentglobal = await messagessentglobalcursor.fetchone()
    messagessentglobal = messagessentglobal[0]
    await messagessentglobalcursor.close()

    xpglobalcursor = await connection.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (0, message.author.id))
    xpglobal = await xpglobalcursor.fetchone()
    xpglobal = xpglobal[0]
    await xpglobalcursor.close()

    await connection.execute("UPDATE membertable set messagessent = ? WHERE guildid = ? AND memberid = ?", (messagessentglobal + 1, 0, message.author.id))
    await connection.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpglobal + 1, 0, message.author.id))
    await connection.commit()
    await connection.close()

async def new_minute_in_vc(bot):
    for guild in bot.guilds:
        for vc in guild.voice_channels:
            for member in vc.members:
                if member.bot == False and len(member.voice.channel.members) > 1:
                    file_name = "./database/database.db"
                    connection = await aiosqlite.connect(file_name) #connect to polldatabase
                    await connection.execute("CREATE TABLE IF NOT EXISTS membertable (guildid INTEGER, memberid INTEGER, messagessent INTEGER, voicetime INTEGER, xp INTEGER, status TEXT, joinedintosystem TEXT)") #creates a table
                    #print(f"{member.guild.id} || {member.id}")

                    membercursor = connection.execute("SELECT * FROM membertable WHERE guildid = ? AND memberid = ?", (member.guild.id, member.id))
                    member = await membercursor.fetchone()
                    await membercursor.close()

                    if member is not None:
                        
                        voicetimeguildcursor = await connection.execute("SELECT voicetime FROM membertable WHERE guildid = ? AND memberid = ?", (member.guild.id, member.id))
                        voicetimeguild = await voicetimeguildcursor.fetchone()
                        voicetimeguild = voicetimeguild[0]
                        await voicetimeguildcursor.close()

                        xpguildcursor = await connection.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (member.guild.id, member.id))
                        xpguild = await xpguildcursor.fetchone()
                        xpguild = xpguild[0]
                        await xpguildcursor.close()

                        await connection.execute("UPDATE membertable set voicetime = ? WHERE guildid = ? AND memberid = ?", (voicetimeguild + 1, member.guild.id, member.id))
                        await connection.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpguild + 5, member.guild.id, member.id))
                        await new_level_ping(bot, member.id, member.guild.id, xpguild, xpguild + 5)

                        voicetimeglobalcursor = await connection.execute("SELECT voicetime FROM membertable WHERE guildid = ? AND memberid = ?", (0, member.id))
                        voicetimeglobal = await voicetimeglobalcursor.fetchone()
                        voicetimeglobal = voicetimeglobal[0]
                        await voicetimeglobalcursor.close()

                        xpglobalcursor = await connection.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (0, member.id))
                        xpglobal = await xpglobalcursor.fetchone()
                        xpglobal = xpglobal[0]
                        await xpglobalcursor.close()

                        await connection.execute("UPDATE membertable set voicetime = ? WHERE guildid = ? AND memberid = ?", (voicetimeglobal + 1, 0, member.id))
                        await connection.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpglobal + 1, 0, member.id))           
                    else:
                        new_member(member)
                    connection.commit()
                    connection.close()

async def rankcommand(interaction, bot, mentionedmember): #command to check level/status
    #v2:
    #guild_id = interaction.guild.id
    await interaction.response.defer(thinking=True)
    member_id = 0
    if mentionedmember == None:
        member = interaction.user
    else:
        #if (mentionedmember[:2] + mentionedmember[-1]) == "<@>":
        #    member_id = int(mentionedmember[2:-1])
        #else:
        #    member_id = int(mentionedmember)
        #guild = bot.get_guild(guild_id)
        #member = guild.get_member(member_id)
        member = mentionedmember
    #if member == None:
    #    interaction.response.send_message(f"There was never such a member on the server!")
    try:
        guildid = member.guild.id
    except AttributeError:
        guildid = 0
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name) #connect to polldatabase
    cursor = connection.cursor()
    
    cursor.execute("SELECT messagessent FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, member.id))
    messagessentguild = next(cursor, [None])[0]
    cursor.execute("SELECT voicetime FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, member.id))
    voicetimeguild = next(cursor, [None])[0]
    cursor.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, member.id))
    xpguild = next(cursor, [None])[0]
    level = math.floor((xpguild ** 0.5) / 5) #f(x) = x^0.5 / 5 => 5 * f(x) = x^0.5 => log5 * f(x) (0.5) = x
    # Create the embed
    embed = discord.Embed(title=f'Level {level}', description=f'{xpguild} XP', color=discord.Color.green())
    if member.bot:
        embed.set_author(name=member.display_name)
    else:
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
    rank = await checkleaderboard(interaction, member.id)
    embed.add_field(name="Place:", value = f"#{rank}", inline=False)
    embed.add_field(name="Voicetime:", value = str(voicetimeguild) + " minutes", inline=False)
    embed.add_field(name="Messages sent:", value = str(messagessentguild) + " messages", inline=False)
    embed.set_footer(text="Requested by: {}".format(interaction.user.display_name))
    
    # Send the embed
    #member.avatar.save("D:/Coding/Discordbot/ModNPC_in_developement/testfiles/rankcard/pfptest.png")
    await member.display_avatar.save(fp=f"./database/rankcards/profilepictures/{guildid}/{member.id}.png")
    #print(f"\n{file}\n")
    rankcardgenerator(interaction.user.display_name, member.id, rank, xpguild, level, guildid)
    file = discord.File(f"./database/rankcards/generated/{guildid}/{member.id}.png")
    #await interaction.followup.send(file = file)
    await interaction.followup.send(embed=embed)

    #v1:
    #server_id = ctx.guild.id
    #member_id = 0
    #if mentionedmember == None:
    #    member_id = ctx.author.id
    #    member = ctx.author
    #else:
    #    if (mentionedmember[:2] + mentionedmember[-1]) == "<@>":
    #        member_id = int(mentionedmember[2:-1])
    #    else:
    #        member_id = int(mentionedmember)
    #    member = ctx.guild.get_member(member_id)
    #file_name = "./database/database.json"
    #with open(file_name, 'r', encoding = 'utf-8') as f:
    #    data = json.load(f)
    #xp = data["stats"][0]["xp"]
    #level = math.floor((xp ** 0.5) / 5)
    #voicetime = data["stats"][0]["voicetime"]
    #messagessent = data["stats"][0]["messagessent"]
    # Create the embed
    #embed = discord.Embed(title=f'Level {level}', description=f'{xp} XP', color=discord.Color.green())
    #embed.set_author(name=member.display_name, icon_url=member.avatar.url)
    #embed.add_field(name="Voicetime:", value = str(voicetime) + " minutes", inline=False)
    #embed.add_field(name="Messages sent:", value = str(messagessent) + " messages", inline=False)
    #embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    # Send the embed
    #await ctx.send(embed=embed)

async def setlevelpingchannelcommand(interaction, channel):
        if interaction.user.guild_permissions.administrator:
            filename = "./database/database.db"
            connection = sqlite3.connect(filename) #connect to polldatabase
            cursor = connection.cursor()
            if (cursor.execute("SELECT * FROM guildsetup WHERE guildid = ?", (interaction.guild.id,)).fetchone()) is not None:
                cursor.execute("UPDATE guildsetup set levelingsystemstatus = ? AND levelingpingmessagechannel = ? WHERE guildid = ?", (True, channel.id, interaction.guild.id))
                await interaction.response.send_message(f"The level ping was set in {channel.name}", ephemeral = True)
                connection.commit()
                connection.close()
            else:
                await interaction.response.send_message("There is an error. Please go on our supportserver and post your problem in the forum. The developer will help you. \n ERRORCODE: 000001", ephemeral = True)
        else:
            await interaction.response.send_message("You don't have the rights to set the levelpingchannel.", ephemeral = True)

async def new_level_ping(bot, memberid, guildid, xpbefore, xpafter): #called every time a member get xp
    oldlevel = math.floor((xpbefore ** 0.5) / 5)
    newlevel = math.floor(((xpafter) ** 0.5) / 5)
    if oldlevel < 0:
        oldlevel = 0
    if newlevel < 0:
        newlevel = 0
    if oldlevel != newlevel and memberid != bot.user.id:
        filename = "./database/database.db"
        connection = sqlite3.connect(filename) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("SELECT levelingsystemstatus FROM guildsetup WHERE guildid = ?", (guildid,))
        levelingsystemstatus = next(cursor, [None])[0]
        if levelingsystemstatus == True:
            cursor.execute("SELECT levelingpingmessagechannel FROM guildsetup WHERE guildid = ?", (guildid,))
            channelid = next(cursor, [None])[0]
            channel = await bot.fetch_channel(channelid)
            if cursor.execute("SELECT * FROM levelroles WHERE guildid = ? AND level = ?", (guildid, newlevel)).fetchone() is not None:
                cursor.execute("SELECT roleid FROM levelroles WHERE guildid = ? AND level = ?", (guildid, newlevel))
                roleid = next(cursor, [None])[0]
                guild = bot.get_guild(guildid) #getting guild
                member = guild.get_member(memberid) #getting member
                role = discord.utils.get(guild.roles, id=roleid)
                await member.add_roles(role)
                oldroles = cursor.execute("SELECT roleid FROM levelroles WHERE guildid = ? AND level < ? AND keeprole = 0", (guildid, newlevel)).fetchall()
                if oldroles is not None:
                    await member.remove_roles(oldroles)
                embed = discord.Embed(title=f'Congratulations!!!', description=f'<@{memberid}> reached level {newlevel} and got the role `{role.name}`.', color=discord.Color.green())
            else:
                embed = discord.Embed(title=f'Congratulations!!!', description=f'<@{memberid}> reached level {newlevel}.', color=discord.Color.green())
            await channel.send(embed=embed)
        connection.close()

async def getlevelrole(bot, memberid, guildid, level):
    filename = "./database/database.db"
    connection = sqlite3.connect(filename) #connect to polldatabase
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS levelroletable (guildid INTEGER, level INTEGER, roleid INTEGER, keepit BOOLEAN)")
    if cursor.execute("SELECT * FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level)).fetchone() is not None:
        cursor.execute("SELECT roleid FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level))
        roleid = next(cursor, [None])[0]
        guild = bot.get_guild(guildid) #getting guild
        member = guild.get_member(memberid) #getting member
        role = discord.utils.get(guild.roles, id=roleid)
        await member.add_roles(role)
        roles = cursor.execute("SELECT roleid FROM levelroletable WHERE guildid = ? AND level < ? AND keepit = 0", (guildid, level)).fetchall()
        if roles != None:
            await member.remove_roles(roles)
        return(role)
    else:
        return(None)
    
async def add_level_role_command(interaction, level, role, keepit):
    filename = "./database/database.db"
    connection = sqlite3.connect(filename) #connect to polldatabase
    cursor = connection.cursor()
    guildid = interaction.guild.id
    if cursor.execute("SELECT * FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level)).fetchone() is None:
        cursor.execute("INSERT INTO levelroletable VALUES (?, ?, ?, ?)", (guildid, level, role.id, keepit)) #write into the table the data
        await interaction.response.send_message(f"Success. The levelrole {role} was added to level {level}.", ephemeral=True)

async def remove_level_role_command(interaction, level):
    filename = "./database/database.db"
    connection = sqlite3.connect(filename) #connect to polldatabase
    cursor = connection.cursor()
    guildid = interaction.guild.id
    if cursor.execute("SELECT * FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level)).fetchone() is not None:
        cursor.execute("DELETE FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level))
        await interaction.response.send_message(f"Success. The levelrole was removed from level {level}.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Error. There isnt a levelrole at level {level}.", ephemeral=True)

async def checkleaderboard(interaction, memberid = None):
    filename = "./database/database.db"
    async with aiosqlite.connect(filename) as connection:
        cursor = await connection.cursor()
        try:
            guildid = interaction.guild.id
        except AttributeError:
            guildid = 0
        if memberid is not None:
            # Check rank for a specific member
            await cursor.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, memberid))
            row = await cursor.fetchone()
            if row is not None:
                xp = row[0]
                # Count members with more XP than the searched member
                await cursor.execute("SELECT COUNT(*) FROM membertable WHERE guildid = ? AND xp > ?", (guildid, xp))
                place = await cursor.fetchone()
                return place[0] + 1
            else:
                return None  #Member not found
        else:
            # Get leaderboard for the guild
            i = 1
            max_xp = 99999999999999
            embed = discord.Embed(title='Leaderboard:', color=discord.Color.green())
            guild = interaction.guild
            while i <= 10:
                await cursor.execute("SELECT xp, memberid FROM membertable WHERE guildid = ? AND xp < ? ORDER BY xp DESC", (guildid, max_xp))
                row = await cursor.fetchone()
                if row:
                    xp, memberid = row
                    if guildid != 0:
                        member = guild.get_member(memberid)
                        memberdisplayname = member.display_name
                        if member:
                            embed.add_field(name=f"Place #{i}:", value=memberdisplayname, inline=False)
                            i += 1
                        max_xp = xp
                    else:
                        memberdisplayname = f"<@{memberid}>"
                        if memberdisplayname:
                            embed.add_field(name=f"Place #{i}:", value=memberdisplayname, inline=False)
                            i += 1
                        max_xp = xp
                else:
                    break  # No more results
            await interaction.response.send_message(embed=embed)

async def addxp2user(interaction, bot, xptoadd, mentionedmember):
    member = interaction.user
    if await check4dm(interaction) == False and member.guild_permissions.administrator:
        if mentionedmember != None:
            member = mentionedmember
        #v2:
        filename = "./database/database.db"
        connection = sqlite3.connect(filename) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (member.guild.id, member.id))
        xpguild = next(cursor, [None])[0]
        cursor.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpguild + xptoadd, member.guild.id, member.id))
        await new_level_ping(bot, member.id, member.guild.id, xpguild, xpguild + xptoadd)
        connection.commit()
        connection.close()
        #v1:
        #file_name = "./Member/" + str(ctx.guild.id) + "/" + str(member_id) + ".json"
        #with open(file_name, 'r', encoding = 'utf-8') as f:
        #    data = json.load(f)
        #xp = data["stats"][0]["xp"]
        #data["stats"][0]["xp"] = xp + int(xptoadd)
        #with open(file_name, 'w', encoding = 'utf-8') as f:
        #    json.dump(data, f, indent = 1)
        #    f.close()
        embed = discord.Embed(title=f'Success', description=f"You have added <@{member.id}> {xptoadd} xp and this member now has {xpguild + int(xptoadd)} xp.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=f'Error', description=f"You don't have the permissions to give anyone xp.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral = True)

async def removexpfromuser(interaction, bot, xptoremove, mentionedmember):
    member = interaction.user
    if await check4dm(interaction) and member.guild_permissions.administrator:
        if mentionedmember != None:
            member = mentionedmember
        #v2:
        filename = "./database/database.db"
        connection = sqlite3.connect(filename) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (interaction.guild.id, member.id))
        xpguild = next(cursor, [None])[0]
        cursor.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpguild - xptoremove, interaction.guild.id, member.id))
        await new_level_ping(bot, member.id, interaction.guild.id, xpguild, xpguild - xptoremove)
        connection.commit()
        connection.close()
        #v1:
        #file_name = "./Member/" + str(ctx.guild.id) + "/" + str(member_id) + ".json"
        #with open(file_name, 'r', encoding = 'utf-8') as f:
        #    data = json.load(f)
        #xp = data["stats"][0]["xp"]
        #data["stats"][0]["xp"] = xp - int(xptoremove)
        #with open(file_name, 'w', encoding = 'utf-8') as f:
        #    json.dump(data, f, indent = 1)
        #    f.close()
        embed = discord.Embed(title=f'Succes', description=f"You have removed from <@{member.id}> {xptoremove} xp and this member now has {xpguild - int(xptoremove)} xp.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=f'Error', description=f"You don't have the permissions to remove from anyone xp.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

async def claimcommand(interaction):
    connection = await aiosqlite.connect("./database/database.db")
    memberid = interaction.user.id
    guildid = interaction.guild.id
    lastupvotecursor = await connection.execute('SELECT last_upvote FROM membertable WHERE guildid = ? AND memberid = ?', (0, memberid))
    lastupvote = await lastupvotecursor.fetchone()
    lastupvote = lastupvote[0]
    if lastupvote == None:
        lastupvote = 0
    guildupvotecursor = await connection.execute('SELECT last_upvote FROM membertable WHERE guildid = ? AND memberid = ?', (guildid, memberid))
    guildupvote = await guildupvotecursor.fetchone()
    guildupvote = guildupvote[0]
    if guildupvote == None:
        guildupvote = 0
    now = datetime.now()
    time = int(round((now - datetime(1970, 1, 1)).total_seconds()))
    if guildupvote <= lastupvote:
        await connection.execute("UPDATE membertable set last_upvote = ? WHERE guildid = ? AND memberid = ?", (time, guildid, memberid))
        xpcursor = await connection.execute('SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?', (0, memberid))
        xp = await xpcursor.fetchone()
        xp = xp[0]
        await connection.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xp + 100, guildid, memberid))
        await xpcursor.close()
    await lastupvotecursor.close()
    await guildupvotecursor.close()
    await connection.commit()
    await connection.close()
    embed = discord.Embed(title="Thanks for upvoting!!!", description="Here is the link to upvote: https://discordbotlist.com/bots/modnpc/upvote")
    await interaction.response.send_message(embed=embed)

def rankcardgenerator(username, memberid, rank, xp, level, guildid):
    # Load the background image (replace with your own image)
    background_image_path = f"database/rankcards/backgrounds/{guildid}/{memberid}.png"
    background_image = Image.open(background_image_path).convert("RGBA")

    pfp = Image.open("./database/rankcards/profilepictures/1128824578848862228/945785058676072448.png").convert("RGBA")
    #pfp = avatarfile.convert("RGBA")
    #pfp = pfp.resize((480, 480))
    pfp = ImageOps.fit(pfp, (480, 480), method=Image.Resampling.BICUBIC, bleed=0.0, centering=(0.5, 0.5))
    offset = 0
    blur_radius = 5
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pfp.size[0] - offset, pfp.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    pfp = pfp.copy()
    pfp.putalpha(mask)

    background_image.paste(pfp, (75, 75), pfp)

    progressbarfront = Image.open("./database/rankcards/textures/progressbarfront.png").convert("RGBA")

    # Load a font (choose a font of your preference)
    font_path = "arial.ttf"
    font_size = 80
    font = ImageFont.truetype(font_path, font_size)


    # User's rank details (customize as needed)
    user_name = username
    user_rank = rank
    old_level = level
    new_level = level + 1
    percent = (25 * new_level**5 - xp) / (25 * new_level**5 - 25 * old_level**5)

    percent_position = (837, 45)
    

    # change width of progress bar based on percentage
    progressbarfront = progressbarfront.resize((1675, 80))
    progressbarfront = progressbarfront.resize((round(progressbarfront.size[0] * percent / 100), progressbarfront.size[1]))
    progressbar = Image.open("./database/rankcards/textures/progressbarback.png").convert("RGBA")
    progressbar = progressbar.resize((1675, 80))
    progressbar = ImageOps.expand(progressbar, border=5, fill=(255,255,255))
    progressbar.paste(progressbarfront, (5, 5), progressbarfront)
    drawprogressbar = ImageDraw.Draw(progressbar)
    drawprogressbar.text(percent_position, f"{percent}%", fill="white", anchor="mm", font=font)
    if old_level/10 >= 1:
        if old_level/100 >= 1:
            if old_level/1000 >= 1:
                pass
            else:
                old_level_position = (100, 0)
        else:
            old_level_position = (60, 0)
    else:
        old_level_position = (20, 0)
    drawprogressbar.text(old_level_position, f"{old_level}", fill="white", font=font)

    if new_level/10 >= 1:
        if new_level/100 >= 1:
            if new_level/1000 >= 1:
                pass
            else:
                new_level_position = (1535, 0)
        else:
            new_level_position = (1575, 0)
    else:
        new_level_position = (1615, 0)
    drawprogressbar.text(new_level_position, f"{new_level}", fill="white", font=font)

    # draw progress bar from x,y 50 of background image
    background_image.paste(progressbar, (630, 400), progressbar)

    # Create a drawing context
    draw = ImageDraw.Draw(background_image)

    # Position to draw the user's name
    name_position = (630, 150)
    draw.text(name_position, f"{user_name}", fill="white", font=font)

    # Position to draw the user's rank
    rank_position = (630, 225)
    draw.text(rank_position, f"Rank: #{user_rank}", fill="white", font=font)

    # Position to draw the user's score
    total_xp_position = (630, 300)
    draw.text(total_xp_position, f"Total XP: {xp}", fill="white", font=font)

    background_image.save(f"./database/rankcards/generated/{guildid}/{memberid}.png")
