import os
import math
import discord
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageShow
from math import floor
import unicodedata
import contextlib

#own modules:
from membermanagement import new_member
from link2id import channellink2channelid, channellink2guildid, link2channelid, link2messageid
from checks import check4dm, check4dm_message
from sqlitehandler import change_xp_by, get_lastupvote, update_voicetime, update_lastupvote, update_messagecounter ,asqlite_insert_data, asqlite_pull_data, asqlite_update_data, get_xp_voicetime_messagessent

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
    member = message.author
    try:
        guildids = [0, message.guild.id]
    except AttributeError:
        guildids = [0]
    registeredmember = None
    if member.bot == False:
        registeredmember = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildids[1]} AND memberid = {member.id}", data_to_return="memberid")
        if registeredmember is not None:
            xptomodify=floor(len(message.content)/20)+1
            #"SELECT memberid FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, member.id)
            for guildid in guildids:
                await update_messagecounter(bot=bot, guildid=guildid, memberid=member.id)

                xp = await change_xp_by(bot=bot, guildid=guildid, memberid=member.id, xptomodify=xptomodify)
                
                if guildid != 0:
                    await new_level_ping(bot, member.id, guildid, xp, xp + xptomodify)
        else:
            await new_member(member, bot)    

async def new_minute_in_vc(bot):
    for guild in bot.guilds:
        guildids = [0, guild.id]
        for vc in guild.voice_channels:
            for member in vc.members:
                registeredmember = None
                if member.bot == False:
                    registeredmember = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildids[1]} AND memberid = {member.id}", data_to_return="memberid")
                    if registeredmember is not None:
                        xptomodify=2
                    #"SELECT memberid FROM membertable WHERE guildid = ? AND memberid = ?", (guildid, member.id)
                        for guildid in guildids:
                            await update_voicetime(bot=bot, guildid=guildid, memberid=member.id)

                            xp = await change_xp_by(bot=bot, guildid=guildid, memberid=member.id, xptomodify=xptomodify)

                            if guildid != 0:
                                await new_level_ping(bot, member.id, guildid, xp, xp + xptomodify)
                    else:
                        await new_member(member, bot)

#async def check4voiceactivity(member):
#    if 1 == os.random

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

    #messagessent = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND memberid = {member.id}", data_to_return="messagessent")
    #voicetime = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND memberid = {member.id}", data_to_return="voicetime")
    xp, voicetime, messagessent = await get_xp_voicetime_messagessent(bot=bot, guildid=guildid, memberid=member.id)

    level = math.floor((xp ** 0.5) / 5) #f(x) = x^0.5 / 5 => 5 * f(x) = x^0.5 => log5 * f(x) (0.5) = x
    rank = await checkleaderboard(interaction, bot, member.id)
    

    #for debugging can be used:
    # Create the embed
    #embed = discord.Embed(title=f'Level {level}', description=f'{xp} XP', color=discord.Color.green())
    #if member.bot:
    #    embed.set_author(name=member.display_name)
    #else:
    #    embed.set_author(name=member.display_name, icon_url=member.avatar.url)

    #embed.add_field(name="Place:", value = f"#{rank}", inline=False)
    #embed.add_field(name="Voicetime:", value = str(voicetime) + " minutes", inline=False)
    #embed.add_field(name="Messages sent:", value = str(messagessent) + " messages", inline=False)
    #embed.set_footer(text="Requested by: {}".format(interaction.user.display_name))
    
    # Send the embed
    #member.avatar.save("D:/Coding/Discordbot/ModNPC_in_developement/testfiles/rankcard/pfptest.png")
    await member.display_avatar.save(fp=f"./database/rankcards/profilepictures/{guildid}/{member.id}.png")
    print(member.guild_avatar)
    #print(f"\n{file}\n")
    bot = interaction.client
    rankcardgenerator(bot, member.display_name, member.id, rank, xp, level, guildid)
    file = discord.File(f"./database/rankcards/generated/{guildid}/{member.id}.png")
    os.remove(f"./database/rankcards/profilepictures/{guildid}/{member.id}.png")
    #await interaction.followup.send(file = file, view=rankcardbuttons(bot, owner=member, rankcard=file))
    await interaction.followup.send(file=file)
    os.remove(f"./database/rankcards/generated/{guildid}/{member.id}.png")

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

async def new_level_ping(bot, memberid, guildid, xpbefore, xpafter): #called every time a member get xp
    oldlevel = math.floor((xpbefore ** 0.5) / 5)
    newlevel = math.floor(((xpafter) ** 0.5) / 5)
    if oldlevel < 0:
        oldlevel = 0
    if newlevel < 0:
        newlevel = 0
    channelid = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM guildsetup WHERE guildid = {guildid}", data_to_return="levelingpingmessagechannel")  
    if channelid is None:
        return()
    if oldlevel < newlevel and memberid != bot.user.id: #gets xp
        guild = bot.get_guild(guildid) #getting guild
        member = guild.get_member(memberid) #getting member
        embed = discord.Embed(title=f'Congratulations!!!', description=f'{member.mention} reached level {newlevel}.', color=discord.Color.green())
        roleid = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM levelroles WHERE guildid = {guildid} AND level = {newlevel}", data_to_return="roleid")
        if roleid is not None:
            role = guild.get_role(roleid)
            await member.add_roles(role)
            embed.add_field(name="You achieved a new role:", value=role.mention)
        oldlevels = list(range(0, oldlevel))
        for level in oldlevels:
            status = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM levelroles WHERE guildid = {guildid} AND level = {level}", data_to_return="keeprole")
            if status == True:
                roleid = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM levelroles WHERE guildid = {guildid} AND level = {level}", data_to_return="roleid") 
                role = guild.get_role(roleid)
                await member.remove_roles(role)
        channel = await bot.fetch_channel(channelid)
        await channel.send(embed=embed)

    elif oldlevel > newlevel and memberid != bot.user.id: #looses xp
        levels = list(range(newlevel, oldlevel))
        for level in levels:
            status = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM levelroles WHERE guildid = {guildid} AND level = {level}", data_to_return="keeprole")
            if status == True:
                roleid = await asqlite_pull_data(bot = bot, statement=f"SELECT * FROM levelroles WHERE guildid = {guildid} AND level = {level}", data_to_return="roleid") 
                role = guild.get_role(roleid)
                await member.remove_roles(role)

async def checkleaderboard(interaction, bot, memberid = None):
    try:
        guildid = interaction.guild.id
    except AttributeError:
        guildid = 0
    if memberid is not None:
        # Check rank for a specific member
        xp = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND memberid = {memberid}", data_to_return="xp")
        if xp is not None:
            # Count members with more XP than the searched member
            async with bot.pool.acquire() as connection:
                countercursor = await connection.execute("SELECT COUNT(*) FROM membertable WHERE guildid = ? AND xp > ?", (interaction.guild.id, xp))
                counter = await countercursor.fetchone()
                place = counter[0]
            return(place)
        else:
            return None  #Member not found
    else:
        # Get leaderboard for the guild
        i = 1
        max_xp = 99999999999999
        embed = discord.Embed(title='Leaderboard:', color=discord.Color.green())
        guild = interaction.guild
        while i <= 10:
            #rowcursor = await connection.execute("SELECT * FROM membertable WHERE guildid = ? AND xp < ? ORDER BY xp DESC", (guildid, max_xp))
            xp = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND xp < {max_xp} ORDER BY xp DESC", data_to_return="xp")
            memberid = await asqlite_pull_data(bot=bot, statement=f"SELECT * FROM membertable WHERE guildid = {guildid} AND xp < {max_xp} ORDER BY xp DESC", data_to_return="memberid")
            if memberid:
                if guildid == 0:
                    member = bot.get_member(memberid)
                    memberdisplayname = member.display_name
                    if member:
                        embed.add_field(name=f"Place #{i}:", value=memberdisplayname, inline=False)
                        i += 1
                    max_xp = xp
                else:
                    member = guild.get_member(memberid)
                    if member is not None:
                        embed.add_field(name=f"Place #{i}:", value=member.mention, inline=False)
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
        xp = await change_xp_by(bot=bot, guildid=interaction.guild.id, memberid=member.id, xptomodify=xptoadd)

        await new_level_ping(bot, member.id, member.guild.id, xp-xptoadd, xp)
        
        #v2:
        #filename = "./database/database.db"
        #connection = sqlite3.connect(filename) #connect to polldatabase
        #cursor = connection.cursor()
        #cursor.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (member.guild.id, member.id))
        #xpguild = next(cursor, [None])[0]
        #cursor.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpguild + xptoadd, member.guild.id, member.id))
        #await new_level_ping(bot, member.id, member.guild.id, xpguild, xpguild + xptoadd)
        #connection.commit()
        #connection.close()
        #v1:
        #file_name = "./Member/" + str(ctx.guild.id) + "/" + str(member_id) + ".json"
        #with open(file_name, 'r', encoding = 'utf-8') as f:
        #    data = json.load(f)
        #xp = data["stats"][0]["xp"]
        #data["stats"][0]["xp"] = xp + int(xptoadd)
        #with open(file_name, 'w', encoding = 'utf-8') as f:
        #    json.dump(data, f, indent = 1)
        #    f.close()
        embed = discord.Embed(title=f'Success', description=f"You have added <@{member.id}> {xptoadd} xp and this member now has {xp} xp.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=f'Error', description=f"You don't have the permissions to give anyone xp.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral = True)

async def removexpfromuser(interaction, bot, xptoremove, mentionedmember):
    member = interaction.user
    if await check4dm(interaction) == False and member.guild_permissions.administrator:
        if mentionedmember != None:
            member = mentionedmember
        xp = await change_xp_by(bot=bot, guildid=interaction.guild.id, memberid=member.id, xptomodify=(-xptoremove))

        #await new_level_ping(bot, member.id, member.guild.id, xp, xp - xptoremove)
        #v2:
        #filename = "./database/database.db"
        #connection = sqlite3.connect(filename) #connect to polldatabase
        #cursor = connection.cursor()
        #cursor.execute("SELECT xp FROM membertable WHERE guildid = ? AND memberid = ?", (interaction.guild.id, member.id))
        #xpguild = next(cursor, [None])[0]
        #cursor.execute("UPDATE membertable set xp = ? WHERE guildid = ? AND memberid = ?", (xpguild - xptoremove, interaction.guild.id, member.id))
        #await new_level_ping(bot, member.id, interaction.guild.id, xpguild, xpguild - xptoremove)
        #connection.commit()
        #connection.close()
        #v1:
        #file_name = "./Member/" + str(ctx.guild.id) + "/" + str(member_id) + ".json"
        #with open(file_name, 'r', encoding = 'utf-8') as f:
        #    data = json.load(f)
        #xp = data["stats"][0]["xp"]
        #data["stats"][0]["xp"] = xp - int(xptoremove)
        #with open(file_name, 'w', encoding = 'utf-8') as f:
        #    json.dump(data, f, indent = 1)
        #    f.close()
        embed = discord.Embed(title=f'Success', description=f"You have removed from <@{member.id}> {xptoremove} xp and this member now has {xp} xp.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=f'Error', description=f"You don't have the permissions to remove from anyone xp.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

async def claimcommand(interaction):
    memberid = interaction.user.id
    guildid = interaction.guild.id
    bot = interaction.client
    lastupvote = await get_lastupvote(bot=bot, guildid=0, memberid=memberid)
    if lastupvote == None:
        lastupvote = 0
    guildupvote = await get_lastupvote(bot=bot, guildid=guildid, memberid=memberid)
    if guildupvote == None:
        guildupvote = 0
    now = datetime.now()
    time = int(round((now - datetime(1970, 1, 1)).total_seconds()))
    print(time)
    if guildupvote <= lastupvote:
        #await update_lastupvote(bot=bot, time=time, guildid=guildid, memberid=memberid)
        await change_xp_by(bot=bot, guildid=guildid, memberid=memberid, xptomodify=100)

    embed = discord.Embed(title="Thanks for upvoting!!!", description="Here is the link to upvote: https://discordbotlist.com/bots/modnpc/upvote")
    await interaction.response.send_message(embed=embed)

def rankcardgenerator(bot, username, memberid, rank, xp, level, guildid):
    background_image_path = f"database/rankcards/backgrounds/{guildid}/{memberid}.png" #2400x600
    if os.path.exists(background_image_path):
        pass
    else:
        background_image_path = "./textures/background.png"

    with Image.open(background_image_path).convert("RGBA") as background_image: # Load the background image
        
        pfp = Image.open(f"./database/rankcards/profilepictures/{guildid}/{memberid}.png").convert("RGBA")
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

        progressbarfront = Image.open("./textures/progressbarfront.png").convert("RGBA")


        font = bot.font.rankcard_arial

        # User's rank details (customize as needed)
        user_name = unicodedata.normalize("NFKD", username)
        user_rank = rank+1
        old_level = level
        new_level = level + 1
        percent = (xp - 25 * old_level**2) / (25 * new_level**2 - 25 * old_level**2) * 100#x=xp, a=newlevel, b=oldlevel; xp/(25a² - 25b²)
        percent = math.floor(percent)
        
        percent_position = (837, 45)


        # change width of progress bar based on percentage
        progressbarfront = progressbarfront.resize((1675, 80))
        progressbarfront = progressbarfront.resize((round(progressbarfront.size[0] * (percent+0.1) / 100), progressbarfront.size[1]))
        progressbar = Image.open("./textures/progressbarback.png").convert("RGBA")
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

class rankcardbuttons(discord.ui.View):
    def __init__(self, bot, owner, rankcard):
        self.bot = bot
        self.owner = owner
        self.rankcard = rankcard
        super().__init__(timeout=None)

    @discord.ui.button(label="Properties", custom_id="properties", disabled=True)
    async def properties(self, interaction: discord.Interaction, button: discord.ui.button):
        member = interaction.user

    @discord.ui.button(label="Change your background", custom_id="changeabackground")
    async def changeabackgroundcallback(self, interaction: discord.Interaction, button: discord.ui.button):
        member = interaction.user
        guild = interaction.guild
        if member.dm_channel is None:
            dmchannel = await member.create_dm()
        dmembed = discord.Embed(description="Please upload a picture and interact afterwards with the buttons.")
        dmembed.set_footer(text="Please note, that NSFW and other problematic content will be deleted and will lead to a report to the discord safety team.", icon_url=None)
        await dmchannel.send(embed=dmembed, view=dmrankcardbuttons(guild))
        embed = discord.Embed(description=f"For updating your rankcard background, I created a directe message with you: {dmchannel.jump_url}. Please upload in the next 5 minutes one in {dmchannel.jump_url} and provide the message link in the popup window. After that the interaction will time out.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Report", custom_id="report", style=discord.ButtonStyle.red, emoji="📢")
    async def reportcallback(self, interaction: discord.Interaction, button: discord.ui.button):
        reportchannel = 1226272957106491462
        member = interaction.user
        guild = interaction.guild
        bot = self.bot
        owner = self.owner
        rankcard = self.rankcard
        if member.id != owner.id:
            channel = bot.get_channel(reportchannel)
            file = discord.File(f"./database/rankcards/generated/{guild.id}/{owner.id}.png")
            embed = discord.Embed(title="New report about background!", description=f"{member.name} ||{member.id}|| just reported the rankcard of {owner.name} in the server `{guild.name}`.")
            await channel.send(embed = embed)
            await channel.send(file = file)
            reportembed = discord.Embed(description=f"Thanks for your report and making this server and discord a better place.")
            await interaction.response.send_message(embed=reportembed, ephemeral=True)
        else:
            errorembed = discord.Embed(description=f"You can't report your own rankcard.")
            await interaction.response.send_message(embed=errorembed, ephemeral=True)

class dmrankcardbuttons(discord.ui.View):
    def __init__(self, guild):
        self.guild = guild
        super().__init__(timeout=300)

    @discord.ui.button(label="Change background", custom_id="changeabackground")
    async def uploadabackground(self, interaction: discord.Interaction, button: discord.ui.button):
        member = interaction.user
        await interaction.response.send_modal(modalchangebackground())

    @discord.ui.button(label="Delete background", custom_id="deleteabackground")
    async def deleteabackground(self, interaction: discord.Interaction, button: discord.ui.button):
        member = interaction.user

class modalchangebackground(discord.ui.Modal, title="Change your background"):
    imagelink = discord.ui.TextInput(label="Enter the link to your new background.", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        imagelink = self.imagelink
        member = interaction.user
        messageid = link2messageid(imagelink)
        message = await member.fetch_message(messageid)

        for attachment in message.attachments:
            if attachment is None:
                errorembed = discord.Embed(description=f"This message doesnt have any images.")
                await interaction.response.send_message(embed=errorembed)
                return()
            else:
                await interaction.response.send_message(f"Somebody sended that things in: {imagelink}, {attachment.content_type}")
                break

        background_image_width = background_image.width
        background_image_height = background_image.height
        if background_image_width == 2400 and background_image_height == 600:
            pass
        elif background_image_width / background_image_height == 4:
            background_image = background_image.resize((2400, 600))
        else:
            cropleftright = (background_image_width-2400) / 2
            croptopbottom = (background_image_height-600) / 2
            background_image = background_image.crop((cropleftright, croptopbottom, cropleftright, croptopbottom))
            background_image = background_image.resize((2400, 600))

#async def setlevelpingchannelcommand(interaction, channel):
#        if interaction.user.guild_permissions.administrator:
#            filename = "./database/database.db"
#            connection = sqlite3.connect(filename) #connect to polldatabase
#            cursor = connection.cursor()
#            if (cursor.execute("SELECT * FROM guildsetup WHERE guildid = ?", (interaction.guild.id,)).fetchone()) is not None:
#                cursor.execute("UPDATE guildsetup set levelingsystemstatus = ? AND levelingpingmessagechannel = ? WHERE guildid = ?", (True, channel.id, interaction.guild.id))
#                await interaction.response.send_message(f"The level ping was set in {channel.name}", ephemeral = True)
#                connection.commit()
#                connection.close()
#            else:
#                await interaction.response.send_message("There is an error. Please go on our supportserver and post your problem in the forum. The developer will help you. \n ERRORCODE: 000001", ephemeral = True)
#        else:
#            await interaction.response.send_message("You don't have the rights to set the levelpingchannel.", ephemeral = True)

#moved to setup command       
#async def getlevelrole(bot, memberid, guildid, level):
#    filename = "./database/database.db"
#    connection = sqlite3.connect(filename) #connect to polldatabase
#    cursor = connection.cursor()
#    if cursor.execute("SELECT * FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level)).fetchone() is not None:
#        cursor.execute("SELECT roleid FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level))
#        roleid = next(cursor, [None])[0]
#        guild = bot.get_guild(guildid) #getting guild
#        member = guild.get_member(memberid) #getting member
#        role = discord.utils.get(guild.roles, id=roleid)
#        await member.add_roles(role)
#        roles = cursor.execute("SELECT roleid FROM levelroletable WHERE guildid = ? AND level < ? AND keepit = 0", (guildid, level)).fetchall()
#        if roles != None:
#            await member.remove_roles(roles)
#        return(role)
#    else:
#        return(None)

#moved to setupcommand    
#async def add_level_role_command(interaction, level, role, keepit):
#    filename = "./database/database.db"
#    connection = sqlite3.connect(filename) #connect to polldatabase
#    cursor = connection.cursor()
#    guildid = interaction.guild.id
#    if cursor.execute("SELECT * FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level)).fetchone() is None:
#        cursor.execute("INSERT INTO levelroletable VALUES (?, ?, ?, ?)", (guildid, level, role.id, keepit)) #write into the table the data
#        await interaction.response.send_message(f"Success. The levelrole {role} was added to level {level}.", ephemeral=True)

#moved to setupcommand    
#async def remove_level_role_command(interaction, level):
#    filename = "./database/database.db"
#    connection = sqlite3.connect(filename) #connect to polldatabase
#    cursor = connection.cursor()
#    guildid = interaction.guild.id
#    if cursor.execute("SELECT * FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level)).fetchone() is not None:
#        cursor.execute("DELETE FROM levelroletable WHERE guildid = ? AND level = ?", (guildid, level))
#        await interaction.response.send_message(f"Success. The levelrole was removed from level {level}.", ephemeral=True)
#    else:
#        await interaction.response.send_message(f"Error. There isnt a levelrole at level {level}.", ephemeral=True)