import os
import json
from datetime import datetime
import discord

#own modules:
from automod import automod
from sqlitehandler import get_logchannelid, get_logwebhookid, update_logwebhookid

#moved to setupcommand:

#async def setlogchannelcommand(interaction, channel):
#    member = interaction.user
#    if member.guild_permissions.administrator:
#        connection = await aiosqlite.connect("./database/database.db")
#        guildid = interaction.guild.id
#        await connection.execute("UPDATE guildsetup set logchannelid = ? WHERE guildid = ?", (channel.id, guildid))
#        await connection.commit()
#        await connection.close()
#        embed = discord.Embed(title = f"This channel was set to the logging channel.", description = f"This action was made by {member.mention} ||{member.id}||.")
#        await channel.send(embed = embed)
#        embed = discord.Embed(title = f"*SUCCESS*", description = f"You set the channel to {channel.mention}.")
#        await interaction.response.send_message(embed = embed, ephemeral = True)
#    else:
#        embed = discord.Embed(title = f"*ERROR*", description = f"You dont have administrator rights.")
#        await interaction.response.send_message(embed = embed, ephemeral = True)

#messages:
async def messagesenteventlog(bot, message):
    eventtype = "sent" 
    
    #connection = await aiosqlite.connect("./database/database.db")
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
    #write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.created_at))

async def messageeditedeventlog(bot, before, after):
    eventtype = "edited"
    if after is None:
        return
    else:
        webhook = await getlogwebhook(bot=bot, guildid=after.guild.id)

        logchannel = None
        if webhook is None:
            logchannel = await getlogchannel(bot, after.guild.id)
        if (logchannel is not None or webhook is not None) and before is not None and after is not None:
            embed = discord.Embed(title = f"{after.author.display_name} ({after.author.id}) just edited the message: {after.jump_url}.")
            embed.add_field(name = f"Before: ({before.created_at})", value = f"```{before.content}```\n\n||Embeds if existing in the thread||", inline = True)
            embed.add_field(name = f"After: ({after.edited_at})", value = f"```{after.content}```\n\n||Embeds if existing in the thread||", inline = True)
            await loginfosandsending(embed, after.author, bot, webhook, logchannel, message1=before, message2=after)
    #v2:
    #write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.edited_at))

async def messagedeletedeventlog(bot, message):
    eventtype="deleted"
    if bot.user.id != message.author.id:
        webhook = await getlogwebhook(bot=bot, guildid=message.guild.id)

        logchannel = None
        if webhook is None:
            logchannel = await getlogchannel(bot, message.guild.id)
        if (logchannel is not None or webhook is not None):

            embed = discord.Embed(title = f"{message.author.display_name} ({message.author.id}) just deleted a message.")
            embed.add_field(name = f"Content: ({message.created_at})", value = f"```{message.content}```\n\n||Embeds and files if existing in the thread||", inline = True)
            files = None
            #if message.attachments is not None:
            #    files=[]
            #    for attachment in message.attachments:
            #        file = await attachment.to_file(filename=f"/database/loggingfiles/{message.id}/")
            #        files.append(file)
            await loginfosandsending(embed, message.author, bot, webhook, logchannel, message1=message, files=files)
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
    #v2:
    #write_into_log(eventtype, message.author.id, message.guild.id, message.channel.id, message.id, message.content, str(message.created_at))

#def write_into_log(eventtype, memberid, guildid, channelid, messageid, content, timestamp):
#    file_name = "./database/database.db"
#    connection = sqlite3.connect(file_name) #connect to polldatabase
#    cursor = connection.cursor()
#    cursor.execute("CREATE TABLE IF NOT EXISTS messagelog (eventtype TEXT, memberid INTEGER, guildid INTEGER, channelid INTEGER, messageid INTEGER, content TEXT, timestamp TEXT)") #creates a table that have the ground data of the poll
#    cursor.execute("INSERT INTO messagelog VALUES (?, ?, ?, ?, ?, ?, ?)", (eventtype, memberid, guildid, channelid, messageid, content, timestamp)) #write into the table the data
#    connection.commit()
#    connection.close()

#voicechat
async def voicechatupdate(bot, member, before, after): #nennt_mich_wie_ihr_wollt | <VoiceState self_mute=False self_deaf=False self_stream=False suppress=False requested_to_speak_at=None channel=<VoiceChannel id=1128824579398307923 name='Allgemein' rtc_region=None position=0 bitrate=64000 video_quality_mode=<VideoQualityMode.auto: 1> user_limit=0 category_id=1128824579398307920>> | <VoiceState self_mute=False self_deaf=False self_stream=False suppress=False requested_to_speak_at=None channel=None>    
    webhook = await getlogwebhook(bot=bot, guildid=after.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, after.guild.id)

    if (logchannel is not None or webhook is not None):
        try:
            beforechannelid = before.channel.id
        except:
            beforechannelid = None
        try:
            afterchannelid = after.channel.id
        except:
            afterchannelid = None

        if beforechannelid != afterchannelid:
            if afterchannelid != None and beforechannelid != None:
                embed = discord.Embed(title = f"{member.display_name} just moved from {before.channel.jump_url} to {after.channel.jump_url}.")
                await before.channel.send(embed=embed)
                await after.channel.send(embed=embed)
            elif afterchannelid != None:
                embed = discord.Embed(title = f"{member.display_name} just joined {after.channel.jump_url}.")
                await after.channel.send(embed=embed)
            elif beforechannelid != None:
                embed = discord.Embed(title = f"{member.display_name} just left {before.channel.jump_url}.")
                await before.channel.send(embed=embed)
            await loginfosandsending(embed, member, bot, webhook, logchannel)
        
        #if beforechannelid != afterchannelid:
        #    embed = discord.Embed(title = f"{member.display_name} just joined a voicechat.")
        #    try:
        #        embed.add_field(name = f"Before: ({before.channel.jump_url})", value = f"name: {before.channel.name}\ntype: {before.channel.type}\nregion: {before.channel.rtc_region}\n", inline = True)
        #    except:
        #        embed.add_field(name = f"Before: (No channel)", value = f"name: No channel\ntype: No channel\nregion: No channel\n", inline = True)
        #    try:
        #        embed.add_field(name = f"After: ({after.channel.jump_url})", value = f"name: {after.channel.name}\ntype: {after.channel.type}\nregion: {after.channel.rtc_region}\n", inline = True)
        #    except:
        #        embed.add_field(name = f"After: (No channel)", value = f"name: No channel\ntype: No channel\nregion: No channel\n", inline = True)   
        #    await loginfosandsending(embed, member, bot, logchannel)

#member
async def memberjoin(bot, member):
    webhook = await getlogwebhook(bot=bot, guildid=member.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, member.guild.id)
    if (logchannel is not None or webhook is not None):
        embed = discord.Embed(title = f"{member.display_name} just joined.")
        await loginfosandsending(embed, member, bot, webhook, logchannel)
    
async def memberleave(bot, payload):
    webhook = await getlogwebhook(bot=bot, guildid=payload.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, payload.guild.id)
    if (logchannel is not None or webhook is not None):
        guild = bot.get_guild(payload.guild_id) #getting guild
        embed = discord.Embed(title = f"{payload.user.display_name} just left.")
        await loginfosandsending(embed, payload.user, bot, webhook, logchannel)
        
async def memberupdate(bot, before, after): #deactivated due to problem with before and after
    print(before)
    print(after)
    guild = ""

    webhook = await getlogwebhook(bot=bot, guildid=after.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, after.guild.id)
    if (logchannel is not None or webhook is not None):

        member = ""
        embed = discord.Embed(title = f"{member.display_name} ({member.id}) just got banned by {logs.user.display_name}.")
        embed.add_field(name = "Reason:", value = logs.reason)
        await loginfosandsending(embed, member, bot, webhook, logchannel)  

async def memberban(bot, guild, member):
    webhook = await getlogwebhook(bot=bot, guildid=member.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, member.guild.id)
    if (logchannel is not None or webhook is not None):
        if guild.me.guild_permissions.view_audit_log:
            async for entry in bot.get_guild(guild.id).audit_logs(action=discord.AuditLogAction.ban):
                if entry.target == member:
                    embed = discord.Embed(title = f"{member.display_name} ({member.id}) just got banned by {entry.user.display_name}.")
                    embed.add_field(name = "Reason:", value = entry.reason)
        else:
            embed = discord.Embed(title = f"{member.display_name} ({member.id}) just got banned.")
            embed.add_field(name = "ATTENTION:", value = "To get more data, look in the audit logs or enable in the bot integration the `view_audit_log` or the `administrator` permission.")
        await loginfosandsending(embed, member, bot, webhook, logchannel)
        
async def memberunban(bot, guild, member):
    webhook = await getlogwebhook(bot=bot, guildid=member.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, member.guild.id)
    if (logchannel is not None or webhook is not None):
        #try:
        if guild.me.guild_permissions.view_audit_log:
            async for logs in bot.get_guild(guild.id).audit_logs(action=discord.AuditLogAction.ban):
                if logs.target == member:
                    embed = discord.Embed(title = f"{member.display_name} ({member.id}) just got unbanned by {logs.user.display_name}.")
                    async for oldlogs in bot.get_guild(guild.id).audit_logs(action=discord.AuditLogAction.ban):
                        if oldlogs.target == member:
                            embed.add_field(name = "Banreason:", value = f"{member.display_name} ({member.id}) got banned from {oldlogs.user} at the date {oldlogs.created_at} for {oldlogs.reason}", inline = False)
        #except:
        else:
            embed = discord.Embed(title = f"{member.display_name} ({member.id}) just got unbanned.")
            embed.add_field(name = "ATTENTION:", value = "To get more data, look in the audit logs or enable in the bot integration the `view_audit_log` or the `administrator` permission.")
        await loginfosandsending(embed, member, bot, webhook, logchannel)

async def invitecreate(bot, invite):
    guild = invite.guild
    webhook = await getlogwebhook(bot=bot, guildid=invite.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, invite.guild.id)
    if (logchannel is not None or webhook is not None):
        if guild.me.guild_permissions.manage_channels:
            member = invite.inviter
            embed = discord.Embed(title = f"{member.display_name} ({member.id}) just created a invite link.")
            if invite.expires_at == 0:
                age = "never"
            else:
                age = invite.expires_at
            if invite.max_uses == 0:
                age = "unlimited"
            else:
                age = invite.expires_at
            embed.add_field(name="Informations:", value = f"Creator: {member}\nMax uses: {invite.max_uses}\nExpires at: {age}\nCode: {invite.code}\nURL: {invite.url}")
            await loginfosandsending(embed, member, bot, webhook, logchannel)

async def invitedelete(bot, invite):
    guild = invite.guild
    webhook = await getlogwebhook(bot=bot, guildid=invite.guild.id)

    logchannel = None
    if webhook is None:
        logchannel = await getlogchannel(bot, invite.guild.id)
    if (logchannel is not None or webhook is not None):
        if guild.me.guild_permissions.manage_channels:
            member = invite.inviter
            embed = discord.Embed(title = f"A invite link was just deleted.")
            embed.add_field(name="Informations:", value = f"Used: {invite.uses}\nCode: {invite.code}\nCreated: {invite.created_at}")
            await loginfosandsending(embed, member, bot, webhook, logchannel)

async def loginfosandsending(embed, member, bot, webhook = None, logchannel = None, message1 = None, message2 = None, files = None):
    try:
        if member.bot:
            embed.set_author(name=f"{member.display_name} ({member.id})")
        else:
            embed.set_author(name=f"{member.display_name} ({member.id})", icon_url=member.avatar.url)
    except:
        pass
    embed.set_footer(text=f"{bot.user.name} | {datetime.utcnow()}")
    if bot.user.id != member.id:
        if webhook is not None:
            logmessage = await webhook.send(embed = embed)
        else:
            logmessage = await logchannel.send(embed = embed)
        if message1 is not None:
            if (message1.embeds != [] and message1.embeds is not None) or files is not None:
                logmessagethread = await logmessage.create_thread(name = "Embeds")
                threadmessage1 = await logmessagethread.send(content = f"Embed of {member.display_name} ({member.id})", embeds = message1.embeds)
                await threadmessage1.pin()
                if message2 is not None:
                    if message2.embeds != [] and message2.embeds is not None:
                        threadmessage2 = await logmessagethread.send(content = f"Embed of {member.display_name} ({member.id})", embeds = message2.embeds)
                        await threadmessage2.pin()
                if files is not None:
                    filesmessage = await logmessagethread.send(content = f"File of {member.display_name} ({member.id})", files = files)
                    await filesmessage.pin()

async def getlogchannel(bot, guildid):
    logchannelid = await get_logchannelid(bot=bot, guildid=guildid)
    logchannel = None
    if logchannelid is not None:
        try:
            logchannel = await bot.fetch_channel(logchannelid)
        except:
            guild = await bot.fetch_guild(guildid)
            dmembed = discord.Embed(description="Due to problems the bot detected while trying to log, we wanted you to remember setting the permissions for the logchannel right.\nPlease activate for the bot these permissions: \n`view channel`\n`manage webhooks`\n`send messages`\n`send messages in threads`\n`create public threads` or the guildpermission `administrator`")
            if guild.owner is not None:
                dmchannel = await guild.owner.create_dm()
                await dmchannel.send(dmembed)
                logchannel = None
    else:
        logchannel = None
    return(logchannel)

async def getlogwebhook(bot, guildid):
    logchannelid = await get_logchannelid(bot=bot, guildid=guildid)
    webhookid = await get_logwebhookid(bot=bot, guildid=guildid)
    logchannel = None
    print(webhookid)
    if webhookid is None:
        try:
            logchannel = await bot.fetch_channel(logchannelid)
            webhook = await logchannel.create_webhook(name="ModNPC Logging", reason="Created Webhook for Logging")
            await update_logwebhookid(bot=bot, logwebhookid=webhook.id, guildid=guildid)
        except:
            guild = await bot.fetch_guild(guildid)
            dmembed = discord.Embed(description="Due to problems the bot detected while trying to log, we wanted you to remember setting the permissions for the logchannel right.\nPlease activate for the bot these permissions: \n`view channel`\n`manage webhooks`\n`send messages`\n`send messages in threads`\n`create public threads` or the guildpermission `administrator`")
            if guild.owner is not None:
                dmchannel = await guild.owner.create_dm()
                await dmchannel.send(dmembed)
        if webhook is not None:
            return(webhook)
        else:
            return(None) #not able to create webhook
    else:
        webhook = await bot.fetch_webhook(webhookid)
        return(webhook)