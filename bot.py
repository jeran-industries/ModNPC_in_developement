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

#own modules:
from on_startup import database_checking_and_creating, message_back_online, beta_message_back_online
from selfroles import create_selfrole, add_selfrole, add_selfrole_2_member, remove_selfrole_from_member, clear_message_from_selfroles, create_selfrole_select_menu, add_selfrole_2_select_menu
from poll import poll_creating, new_pollreaction_4_log, remove_pollreaction_4_log, editingpollafternewreaction, editingpollafterremovedreaction
from levelsystem import new_message, new_minute_in_vc, rankcommand, addxp2user, removexpfromuser, checkleaderboard, setlevelpingchannelcommand, add_level_role_command, remove_level_role_command, claimcommand
from log import messagesenteventlog, messageeditedeventlog, messagedeletedeventlog, voicechatupdate
from membermanagement import new_member
from dice import throwdicecommand
from welcomemessage import sendwelcomemessage
from help import answer4help, answer4help4mods, helpwithsetup
from botupdates import publishbotupdatescommand#, setbotupdateschannelcommand
from sync import synccommand
from anonymousmessage import sendanonymousmessagecommand
from setup import setupcommand
from presence import presenceupdate
from checks import check4upvotebotlist

#from "dateiname" import "name der funktion"

load_dotenv()
TOKEN = os.getenv('Dc_token')
BETA_TOKEN = os.getenv('Dc_token_beta')
BETA_CLIENT_ID = os.getenv('Client_id_beta')
DC_SERVER = os.getenv('Dc_server')
CLIENT_ID = os.getenv('Client_id')
BOTLISTTOKEN = os.getenv('Dc_bot_list_Token')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='/')
#tracemalloc.start()
handler = logging.FileHandler(filename='./database/discord.log', encoding='utf-8')
sys.path.append('.')

#Welcome-Message
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1184497343815499898)
    embed = discord.Embed(title="Welcome!", description=f"{member.mention} just joined")
    await channel.send(embed=embed)
    sendwelcomemessage(member, bot)
    new_member(member)

@tasks.loop(minutes=1)
async def one_minute_loop():
    await new_minute_in_vc(bot)

@tasks.loop(minutes=10)
async def ten_minute_loop():
    await presenceupdate(bot)
    await check4upvotebotlist(bot, BOTLISTTOKEN)

@bot.event
async def on_message(message):
    await bot.process_commands(message) 
    #print(message)
    await messagesenteventlog(message) #messagelog
    await new_message(bot, message) #levelingsystem  
    
@bot.event
async def on_message_edit(before, after):
    messageeditedeventlog(after)

@bot.event
async def on_message_deleted(message):
    messagedeletedeventlog(message)

@bot.event
async def on_voice_state_update(member, before, after):
    await voicechatupdate(member, after, before)

#Simpletestcommand    
@bot.command()
async def status(ctx):
    await ctx.reply('Hi, im here online')

#@bot.command()
#async def Ineedhelp(ctx):
#    await answer4help(ctx)

#@bot.command()
#async def Ineedhelpandamamod(ctx):
#    await answer4help4mods(ctx)

#@bot.command()
#async def Ineedhelpwithsetup(ctx):
#    await helpwithsetup(ctx)

@bot.tree.command()
async def setup(interaction:discord.Interaction):   
    await setupcommand(interaction)

#Selfroles:
#v1: selfroles with reactions
@bot.tree.command(name='create_reactionrole')
async def create_reactionrole(interaction:discord.Interaction, messagecontent: str, channeltopostin: discord.TextChannel): #create a new reactionrole
    await create_selfrole(interaction, messagecontent, channeltopostin)

@bot.tree.command(name='add_reactionrole')
async def add_reactionrole(interaction:discord.Interaction, link: str, emoji: str, role: discord.Role, description: str = None): #create a new reactionrole
    await add_selfrole(interaction, bot, link, emoji, role, description)

@bot.tree.command()
async def create_reactionrole_dropmenu(interaction: discord.Interaction, messagecontent: str, channeltopostin: discord.TextChannel, role: discord.Role, description: str):
    await create_selfrole_select_menu(interaction, messagecontent, channeltopostin, role=role, description=description)

@bot.tree.command()
async def add_reactionrole_dropmenu(interaction:discord.Interaction, link: str, role: discord.Role, description: str = None):
    await add_selfrole_2_select_menu(interaction, bot, link, role, description)

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
    await checkleaderboard(interaction)

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

@bot.event
async def on_command_error(ctx, error):
    await ctx.reply(f"Hey there is an error: {error} \n \n Look up if you did everything right with our help command. If you dont understand and cannot find the error, consider joining my support server and opening a ticket: https://discord.com/channels/1128824578848862228/1191733071532261426")

@bot.event
async def on_guild_join(guild):
    database_checking_and_creating(guild.id)
    for member in guild.members:
        new_member(member)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        if guild.name == DC_SERVER:
            break
    #members = '\n - '.join([member.name for member in guild.members])
    print(f'{bot.user} is connected to the servers with these members:\n')
    guildcounter = 0
    membercounter = 0
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        database_checking_and_creating(guild.id)
        guildcounter = guildcounter + 1
        for member in guild.members:
            new_member(member)
            membercounter = membercounter + 1
            print(member)
    #print(f"These are all appcommands: \n{await bot.tree.sync()}")
    one_minute_loop.start()
    ten_minute_loop.start()
    if bot.user.id == 1144006301765095484: #betabot
        await message_back_online(bot)
    elif bot.user.id == 1183880930201448469: #betabot
        await beta_message_back_online(bot)

#Do u want to debug?
debug = input("Please enter ""debug"", if you want to run the beta of this bot. If not enter something else:\n")
if debug == "debug":
    bot.run(BETA_TOKEN, log_level=logging.DEBUG)    
else:
    bot.run(TOKEN, log_handler=handler)