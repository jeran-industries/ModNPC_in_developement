#bot.py
#Eventtypes: https://discordpy.readthedocs.io/en/stable/api.html
#update your python: python.exe -m pip install --upgrade pip
#check your python:  pip --version
import os
import io
import json                         #install-command: python -m pip install json
import discord                      #install-command: py -3 -m pip install -U discord.py update-command: pip install --upgrade discord.py
from discord.ext import commands, tasks    #install-command: pip install discord.ext.context
from dotenv import load_dotenv      #install-command: pip install python-dotenv
import tracemalloc
import sys
import logging
import time
import math
import aiohttp
import aiosqlite
import asqlite 

#own modules:
from on_startup import database_checking_and_creating, message_back_online, beta_message_back_online
from selfroles import create_selfrole, add_selfrole, add_selfrole_2_member, remove_selfrole_from_member, clear_message_from_selfroles, create_selfrole_select_menu, add_selfrole_2_select_menu, selfrolesaddview
from poll import poll_creating, new_pollreaction_4_log, remove_pollreaction_4_log, editingpollafternewreaction, editingpollafterremovedreaction
from levelsystem import new_message, new_minute_in_vc, rankcommand, addxp2user, removexpfromuser, checkleaderboard, claimcommand
from log import messagesenteventlog, messageeditedeventlog, messagedeletedeventlog, voicechatupdate, memberjoin, memberleave, memberupdate, memberban, memberunban, invitecreate, invitedelete
from membermanagement import new_member
from dice import throwdicecommand
from welcomemessage import sendwelcomemessage
from help import answer4help, answer4help4mods, helpwithsetup
from botupdates import publishbotupdatescommand#, setbotupdateschannelcommand
from sync import synccommand, reconnectcommand, disconnectcommand
from anonymousmessage import sendanonymousmessagecommand
from setup import setupcommand
from presence import presenceupdate
from checks import check4upvotebotlist
from autoroles import add_autorole_2_user, addrole2allmembercommand, removerolefromallmembercommand
from sqlitehandler import asqlite_pull_data, create_guildsetup_table, create_autorole_table, create_levelroles_table, create_member_table

#from "dateiname" import "name der funktion"

load_dotenv()
TOKEN = os.getenv('Dc_token')
BETA_TOKEN = os.getenv('Dc_token_beta')
BETA_CLIENT_ID = os.getenv('Client_id_beta')
DC_SERVER = os.getenv('Dc_server')
CLIENT_ID = os.getenv('Client_id')
BOTLISTTOKEN = os.getenv('Dc_bot_list_Token')
MEMBERLOGCHANNELID = os.getenv('Member_log_channel_ID')
REPORTCHANNELID = os.getenv('Report_channel_ID')
DBLOGCHANNELID = os.getenv('')

#bot = commands.Bot(intents=discord.Intents.all(), command_prefix='/')


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix='/')

    async def setup_hook(self):
        # Load the commands extension
        print("Running setup tasks")
        self.pool = await asqlite.create_pool(database="./database/database.db")
        one_minute_loop.start()
        ten_minute_loop.start()
        print("Running setup tasks completed")
        
bot = MyBot()

#tracemalloc.start()
handler = logging.FileHandler(filename='./database/discord.log', encoding='utf-8')
sys.path.append('.')

#Welcome-Message
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(MEMBERLOGCHANNELID)
    embed = discord.Embed(title="New member!", description=f"{member.mention} just joined to {member.guild.name}")
    await channel.send(embed=embed)
    #await sendwelcomemessage(member, bot)
    await new_member(member, bot)
    await memberjoin(bot, member)
    await add_autorole_2_user(bot=bot, member=member)

@tasks.loop(minutes=1)
async def one_minute_loop():
    print("One minute loop is running")
    await new_minute_in_vc(bot)

@tasks.loop(minutes=10)
async def ten_minute_loop():
    #print("Ten minute loop is running")
    #await presenceupdate(bot)
    await check4upvotebotlist(bot, BOTLISTTOKEN)

@bot.event
async def on_message(message):
    await bot.process_commands(message) 
    #print(message)
    await messagesenteventlog(bot, message) #messagelog
    if message.author.bot == False:
        await new_message(bot, message) #levelingsystem

@bot.event
async def on_message_edit(before, after):
    await messageeditedeventlog(bot, before, after)

@bot.event
async def on_message_delete(message):
    await messagedeletedeventlog(bot, message)

@bot.event
async def on_voice_state_update(member, before, after):
    await voicechatupdate(bot, member, before, after)

#@bot.event
#async def on_member_join(member):
    #await memberjoin(bot, member)

@bot.event
async def on_raw_member_remove(payload):
    await memberleave(bot, payload)

#@bot.event
#async def on_member_update(before, after):
#    await memberupdate(bot, before, after)

@bot.event
async def on_member_ban(guild, user):
    await memberban(bot, guild, user)

@bot.event
async def on_member_unban(guild, user):
    await memberunban(bot, guild, user)

@bot.event
async def on_invite_create(invite):
    await invitecreate(bot, invite)

@bot.event
async def on_invite_delete(invite):
    await invitedelete(bot, invite)

@bot.tree.command()
async def about_me(interaction: discord.Interaction):
    embed = discord.Embed(title = "Here are some interesting links:")
    embed.add_field(name = f"Github Page:", value = f"https://github.com/jeran-industries/modnpc_in_developement", inline = False)
    embed.add_field(name = f"Webdashboard:", value = f"https://jeran.polarlabs.io/modnpc/webdashboard", inline = False)
    embed.add_field(name = f"Privacy Policy:", value = f"https://jeran.polarlabs.io/modnpc/privacy", inline = False)
    embed.add_field(name = f"Terms of Service:", value = f"https://jeran.polarlabs.io/modnpc/tos", inline = False)
    embed.add_field(name = f"Our patreon:heart::", value = f"https://patreon.com/modnpc", inline = False)
    await interaction.response.send_message(embed = embed, delete_after=60)

#add role to all users
@bot.tree.command()
async def add_role_to_all_users(interaction: discord.Interaction, role: discord.Role):
    await addrole2allmembercommand(interaction, role, 0)

#add role to only bots
@bot.tree.command()
async def add_role_to_all_bot_users(interaction: discord.Interaction, role: discord.Role):
    await addrole2allmembercommand(interaction, role, 1)

#add role to only humans
@bot.tree.command()
async def add_role_to_all_human_users(interaction: discord.Interaction, role: discord.Role):
    await addrole2allmembercommand(interaction, role, 2)

#remove role from all users
@bot.tree.command()
async def remove_role_from_all_users(interaction: discord.Interaction, role: discord.Role):
    await removerolefromallmembercommand(interaction, role, 0)

#remove role from only bots
@bot.tree.command()
async def remove_role_from_all_bot_users(interaction: discord.Interaction, role: discord.Role):
    await removerolefromallmembercommand(interaction, role, 1)

#remove role from only humans
@bot.tree.command()
async def remove_role_from_all_human_users(interaction: discord.Interaction, role: discord.Role):
    await removerolefromallmembercommand(interaction, role, 2)

#Simpletestcommand    
@bot.tree.command()
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title = "Pong :ping_pong:")
    embed.add_field(name = f"Latency:", value = f"{math.floor(bot.latency * 1000)} ms", inline = False)
    embed.add_field(name = f"Users:", value = f"{len(bot.users)}", inline = False)
    embed.add_field(name = f"Guilds:", value = f"{len(bot.guilds)}", inline = False)
    await interaction.response.send_message(embed = embed)

#@bot.command()
#async def Ineedhelp(ctx):
#    await answer4help(ctx)

#@bot.command()
#async def Ineedhelpandamamod(ctx):
#    await answer4help4mods(ctx)

#@bot.command()
#async def Ineedhelpwithsetup(ctx):
#    await helpwithsetup(ctx)
    
#setup:
@bot.tree.command()
async def setup(interaction:discord.Interaction):   
    await setupcommand(interaction, bot)

#@bot.tree.command()
#async def log_set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
#    await setlogchannelcommand(interaction, channel)

#Selfroles:
#v1: selfroles with reactions
@bot.tree.command(name='create_reactionrole')
async def reactionrole_create(interaction:discord.Interaction, messagecontent: str, channeltopostin: discord.TextChannel): #create a new reactionrole
    await create_selfrole(interaction, messagecontent, channeltopostin)

@bot.tree.command(name='add_reactionrole')
async def reactionrole_add(interaction:discord.Interaction, link: str, emoji: str, role: discord.Role, description: str = None): #create a new reactionrole
    await add_selfrole(interaction, bot, link, emoji, role, description)

#@bot.tree.command()
#async def reactionrole_create_dropmenu(interaction: discord.Interaction, messagecontent: str, channeltopostin: discord.TextChannel, emoji: str, role: discord.Role, description: str):
#    await create_selfrole_select_menu(bot, interaction, messagecontent, channeltopostin, emoji=emoji, role=role, description=description)

#@bot.tree.command()
#async def reactionrole_add_2_dropmenu(interaction:discord.Interaction, link: str, emoji: str, role: discord.Role, description: str = None):
#    await add_selfrole_2_select_menu(interaction, bot, link, emoji, role, description)

#@bot.help_command()
#async def help(ctx):
#    await answer4help(ctx)

#@bot.command(name='clear_message', description='/clear_message "message_id"') #dont need this just delete the message
#async def clear_message(ctx, link):
#    await clear_message_from_selfroles(ctx, link)
    
#v2: selfroles with selectmenu

#polls
#v2: up to 10 options, votecount and link
@bot.tree.command(name = 'polls', description = 'You can create polls with this command')
#async def polls(ctx, link, votecount, channel_id4poll, option0 = None, option1 = None, option2 = None, option3 = None, option4 = None, option5 = None, option6 = None, option7 = None, option8 = None, option9 = None):
async def polls(interaction:discord.Interaction, message: str, votecount: int, channel: discord.TextChannel, option0: str , option1: str , option2: str = None, option3: str = None, option4: str = None, option5: str = None, option6: str = None, option7: str = None, option8: str = None, option9: str = None):
    await poll_creating(interaction, bot, message, votecount, channel, option0, option1, option2, option3, option4, option5, option6, option7, option8, option9)

#dicethrowing:
@bot.tree.command()
async def throwadice(interaction:discord.Interaction, sides: int, dices: int):
    await throwdicecommand(interaction, sides, dices)

#levelingsystem:
@bot.tree.command(name = "rank")
async def rank(interaction:discord.Interaction, member:discord.Member = None):
    await rankcommand(interaction, bot, member)

@bot.tree.command(name = "addxp")
async def addxp(interaction:discord.Interaction, xp: int, member:discord.Member = None):
    await addxp2user(interaction, bot, xp, member)

@bot.tree.command(name = "removexp")
async def removexp(interaction:discord.Interaction, xp: int, member:discord.Member = None):
    await removexpfromuser(interaction, bot, xp, member)

@bot.tree.command(name = "leaderboard")
async def leaderboard(interaction:discord.Interaction):
    await checkleaderboard(interaction, bot)

@bot.tree.command()
async def claim(interaction:discord.Interaction):
    await claimcommand(interaction)

#@bot.tree.command(name = 'setlevelpingchannel')
#async def setlevelpingchannel(interaction:discord.Interaction, channel:discord.TextChannel):
#    await setlevelpingchannelcommand(interaction, channel)

#@bot.tree.command(name = "add_level_role")
#async def add_level_role(interaction:discord.Interaction, level:int, role:discord.Role, keepit:bool):
#    await add_level_role_command(interaction, level, role, keepit)

#@bot.tree.command(name = "remove_level_role")
#async def remove_level_role(interaction:discord.Interaction, level:int):
#    await remove_level_role_command(interaction, level)

#botupdates:
#@bot.tree.command(name = "set_the_updatechannelcommand")
#async def setbotupdateschannel(interaction: discord.Interaction, channel:discord.TextChannel):
#    await setbotupdateschannelcommand(interaction, channel)

@bot.tree.command(name = "publish_an_updatemessage")
async def publishbotupdatescommand(interaction: discord.Interaction, message:str):
    await publishbotupdatescommand(interaction, bot, message)

@bot.tree.command(name="send_anonymous_message")
async def sendanonymousmessage(interaction: discord.Interaction, message: str, channel:discord.TextChannel):
    await sendanonymousmessagecommand(interaction, message, channel)

@bot.tree.command(name="patreon")
async def patreon(interaction: discord.Interaction):
    embed = discord.Embed(title=f"Hey {interaction.user.display_name}", description="You can look at our patreon on this link: patreon.com/ModNPC")
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def testwelcomemessage(interaction: discord.Interaction, member: discord.Member):
    await sendwelcomemessage(interaction, member=member, bot=bot)

#syncing
@bot.command()
async def sync(ctx):
    await synccommand(ctx, bot, BOTLISTTOKEN)

@bot.command()
async def reconnect(ctx):
    await reconnectcommand(bot)

@bot.command()
async def disconnect(ctx):
    await disconnectcommand(bot)

@bot.command()
async def list(ctx):
    channel = ctx.channel
    list = await channel.webhooks()
    if list is None:
        list = await channel.create_webhook(name= "test", reason = "test")

    await ctx.reply(list)

@bot.tree.command()
async def send_webhook(interaction: discord.Interaction, channel: discord.TextChannel):
    async with aiohttp.ClientSession() as session:
        print(await discord.webhooks())

        e = discord.Embed(title="Title", description="Description")
        e.add_field(name="Field 1", value="Value 1")
        e.add_field(name="Field 2", value="Value 2")

        #await webhook.send(embed=e)

@bot.event
async def on_raw_reaction_add(payload): #reactionadded trigger
    #await new_reaction_4_log(payload, bot)
    await new_pollreaction_4_log(payload, bot)
    #await editingpollafternewreaction(payload, bot)
    await add_selfrole_2_member(bot, payload)

@bot.event
async def on_raw_reaction_remove(payload): #reactionremoved trigger
    #await new_unreaction_4_log(payload, bot)
    await remove_pollreaction_4_log(payload, bot)
    #await editingpollafterremovedreaction(payload, bot)
    await remove_selfrole_from_member(bot, payload)

#@bot.event
#async def on_command_error(ctx, error):
#    await ctx.reply(f"Hey there is an error: {error} \n \n Look up if you did everything right with our help command. If you dont understand and cannot find the error, consider joining my support server and opening a ticket: https://discord.com/channels/1128824578848862228/1191733071532261426")

@bot.event
async def on_guild_join(guild):
    await database_checking_and_creating(bot, guild.id)
    channel = bot.get_channel(MEMBERLOGCHANNELID)
    for channel in guild.channels:
        try:
            inviteurl = await channel.create_invite()
            break
        except:
            pass
    embed = discord.Embed(title="New guild!", description=f"{member.guild.name} just joined the system: {inviteurl}")
    embed.add_field(name="Guildowner", value=guild.owner.name)
    embed.add_field(name="Membercount", value=guild.member_count)
    await channel.send(embed=embed)
    for member in guild.members:
        new_member(member)

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(MEMBERLOGCHANNELID)
    embed = discord.Embed(title="Guild left!", description=f"{member.guild.name} just left the system.")
    embed.add_field(name="Guildowner", value=guild.owner.name)
    embed.add_field(name="Membercount", value=guild.member_count)
    await channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    #for guild in bot.guilds:
    #    if guild.name == DC_SERVER:
    #        break
    #members = '\n - '.join([member.name for member in guild.members])
    print(f'{bot.user} is connected to the servers with these members:\n')
    guildcounter = 0
    membercounter = 0
    await create_guildsetup_table(bot=bot)
    await create_autorole_table(bot=bot)
    await create_levelroles_table(bot=bot)
    await create_member_table(bot=bot)
    #await create_
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        await database_checking_and_creating(bot, guild.id)
        guildcounter = guildcounter + 1
        for member in guild.members:
            #new_member(member, connection)
            membercounter = membercounter + 1
            if member.id != guild.owner_id:
                print(member)
            else:
                print(f"{member} (guildowner)")
    #print(f"These are all appcommands: \n{await bot.tree.sync()}")
    if bot.user.id == 1144006301765095484: #betabot
        await message_back_online(bot)
    elif bot.user.id == 1183880930201448469: #betabot
        await beta_message_back_online(bot)
    await bot.change_presence(status=discord.Status.idle, activity = discord.Game(f"Watching {len(bot.guilds)} servers with {len(bot.users)} members"))

#Do u want to debug?
debug = None

if BETA_TOKEN is None and TOKEN is None:
    print("Hmm looks like the .env file is corrupted or sth like that. Run this command in the terminal on windows python createdotenv.py or on linux python3 createdotenv.py")
elif BETA_TOKEN is None and TOKEN is not None:
    bot.run(TOKEN, log_handler=handler)
elif BETA_TOKEN is not None and TOKEN is None:
    bot.run(BETA_TOKEN, log_level=logging.DEBUG)
else:
    debug = input("Please enter 'debug', if you want to run the beta of this bot. If not enter something else:\n")
    if debug == "debug":
        bot.run(BETA_TOKEN, log_level=logging.DEBUG)
    else:
        bot.run(TOKEN, log_handler=handler)

#runs after bot is out