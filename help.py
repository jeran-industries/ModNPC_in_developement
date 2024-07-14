import discord

async def helpcommand(interaction):
    embed = discord.Embed(title="Choose in which subject you need help!!!")
    await interaction.response.send_message(embed=embed, view=helpbuttons())

class helpbuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(reportissuesbutton())
        self.add_item(supportserverbutton())

    @discord.ui.button(label="Membercommands", custom_id="Membercommands")
    async def membercommands(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(embeds=[await levelingsystemmemberhelp(), await reactionrolesmemberhelp(), await dicesmemberhelp(), await customvoicechatmemberhelp()])

    @discord.ui.button(label="Staffcommands", custom_id="Staffcommands")
    async def staffcommands(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(embeds=[await levelingsystemstaffhelp(), await reactionrolesstaffhelp(), await welcomemessagestaffhelp(interaction), await ticketsystemstaffhelp(), await loggingstaffhelp(), await autorolesstaffhelp()])

#Memberhelp
async def levelingsystemmemberhelp():
    embed = discord.Embed(title="Levelingsystem")
    embed.add_field(name="`/rank`", value="You get send a rankcard with data how much xp you collected, your level and your rank guildwidth.")
    embed.add_field(name="`/leaderboard`", value="You get a list with the top 10 members on the server")
    embed.add_field(name="`/claim`", value="Upvote the bot and run this command to receive 100xp")
    return(embed)

async def reactionrolesmemberhelp():
    embed = discord.Embed(title="Reactionroles")
    embed.add_field(name="How to get a reactionrole?", value="React to a reactionrole message. This is only available if the staff of your server created some.")
    return(embed)

async def dicesmemberhelp():
    embed = discord.Embed(title="Dices")
    embed.add_field(name="`/dices`", value="After entering this command you can decide how much dices you want to throw and how much sides you want to throw.")
    return(embed)

async def customvoicechatmemberhelp():
    embed = discord.Embed(title="Customvoicechat")
    embed.add_field(name="`/cvc_join_request`", value="By entering this command you can request to join a member in a custom voicechat thats locked.")
    return(embed)

#Staffhelp:
async def levelingsystemstaffhelp():
    embed = discord.Embed(title="Levelingsystem")
    embed.add_field(name="`/setup`", value="After entering this command you can choose in the setup command the leveling. You can activate, deactivate, reset, set the levelping channel and modify levelroles. To do this you need administrator rights.")
    embed.add_field(name="`/addxp`", value="You can add to a user xp. If you dont specify a user, you add yourself xp. To do this you need administrator rights.")
    embed.add_field(name="`/removexp`", value="You can remove from a user xp. If you dont specify a user, you remove from yourself xp. To do this you need administrator rights.")
    return(embed)

async def reactionrolesstaffhelp():
    embed = discord.Embed(title="Reactionroles")
    embed.add_field(name="`/create_reactionrole`", value="You can create a reactionroleembed. You can set the messagecontent and the channel it will be posted in. With `/add_reactionrole` you can add reactionroles. To do this you need manage role rights.")
    embed.add_field(name="`/add_reactionrole`", value="You can add reactionrole to an already existing reactionroleembed. For that you need a link to the reactionroleembed, an emoji and a role. You can add a description if needed. To do this you need manage role rights.")
    return(embed)

async def welcomemessagestaffhelp(interaction):
    embed = discord.Embed(title="Welcomemessage")
    embed.add_field(name="`/setup`", value="After entering this command you can choose in the setup command the welcomemessage. You can set the title, content and the channel it will be posted in.\n\n> {member.mention} will be replaced with for example" + f"{interaction.user.mention}\n\n" + "> {member.name} will be replaced with for example " + f"{interaction.user.name}\n\n" + "> {member.display_name} will be replaced with for example " + f"{interaction.user.display_name}\n\nTo do this you need administrator rights.")
    embed.add_field(name="`/testwelcomemessage`", value="You can test the already existing welcomemessage. If the bot doesnt respond it means that you don't have a welcomemessage.")
    return(embed)

async def ticketsystemstaffhelp():
    embed = discord.Embed(title="Ticketsystem")
    embed.add_field(name="`/setup`", value="After entering this command you can choose in the setup command the ticketsystem. You can activate, deactivate and set a channel. To do this you need administrator rights.")
    return(embed)

async def loggingstaffhelp():
    embed = discord.Embed(title="Logging")
    embed.add_field(name="`/setup`", value="After entering this command you can choose in the setup command the logging. You can activate, deactivate and set a channel for logging. To do this you need administrator rights.")
    return(embed)

async def autorolesstaffhelp():
    embed = discord.Embed(title="Autoroles")
    embed.add_field(name="`/setup`", value="After entering this command you can choose in the setup command the autoroles. You can add, remove, reset and list autoroles. If you want to add one, you can choose between human users, bots and all users. To do this you need administrator rights.")
    return(embed)

#Botissues:
class reportissuesbutton(discord.ui.Button):
    def __init__(self, custom_id = "reportissuesbutton"):
        super().__init__(label="Report issues", url = "https://github.com/jeran-industries/ModNPC_in_developement/issues")

class supportserverbutton(discord.ui.Button):
    def __init__(self, custom_id = "supportserverbutton"):
        super().__init__(label="Support Server", url = "https://discord.gg/uWrR9WnfMA")

async def answer4help(ctx):
    embed = discord.Embed(title=f'Hi {ctx.author.name} ({ctx.author.id})', color=discord.Color.yellow())
    embed.add_field(name="Leveling:", value = 'ModNPC collects data about your sent messages and your voicetime. To access your stats, just type `!rank` in. To access the rank of another person, just mention the person or get his memberid. It looks like this: `!rank "memberid or mentioned member"`', inline=False)
    embed.add_field(name="Dicerolling", value = 'Because someone asked for DnD a dicethrowing function we implemented it. Use it with this command: `!throwadice "sides of the dice" "number of dices"`', inline=False)
    embed.add_field(name="You are an admin of this server?", value = 'With `!Ineedhelpandamamod` you can get the commands only you and your adminfriends can use.', inline=False)
    #embed.add_field(name="Selfroles:", value = "You can use ModNPC to add reactionroles or the also called selfroles. This means: By reacting to a message, you can get a selfrole. How do I set that up?: Type in: '/create_reactionrole ""link of the message to add the selfroles"" ""the emoji with which the user reacts"" ""The role that should be added to the user if he reacts""'", inline = True)
    #if ctx.author
    
    await ctx.reply(embed = embed)

async def answer4help4mods(ctx):
    embed = discord.Embed(title=f'Hi {ctx.author.name} ({ctx.author.id})', description = "Warning, you can't use these commands without administrator rights.", color=discord.Color.red())
    embed.add_field(name="Leveling:", value = 'As an administrator you can add xp from a user. For example as a reward. Just use `!addxp "the number of xp you want to add" "the user: you can mention them or enter their memberid"` You can also remove xp: Just use `!removexp "the number of xp you want to remove" "the user: you can mention them or enter their memberid"`', inline = False)
    embed.add_field(name="Polls:", value = 'You can use ModNPC to make surveys. The Pollsystem supports an individual votecount and up to ten options. The command is: `!polls "link to the message that will be posted with the survey." "votecount: votecount means you have multiple choices to take. Voting the same wont work. Choose a number between 1 and 10" "option1" "option2" "option..."` You can stop a poll by reacting to the already posted pausesymbol. Please note that after that the poll can only be resetted. This can be done by reacting to the new symbol.`', inline = False)
    embed.add_field(name="Selfroles:", value = 'You can use ModNPC to add reactionroles(they are also called selfroles). How do I set that up?: Type in: `!create_reactionrole "link of the message to add the selfrole" "the emoji with which the user will react" "The role that should be added to the user if he reacts"` To delete a selfrole, just delete the message and the selfrole wont be seen again for a long, long time', inline = False)
    await ctx.reply(embed = embed)

async def helpwithsetup(ctx):
    embed = discord.Embed(title=f'Hi {ctx.author.name} ({ctx.author.id})', description = "Warning, you can't access the setup without administrator rights.", color=discord.Color.red())
    embed.add_field(name="Leveling:", value = 'ModNPC collects data for leveling even if leveling isnt activated. To add pings if a new level is reached, you need to set a channel for levelpings. Do this with `!setlevelpingchannel "link to the channel".`', inline = False)
    embed.add_field(name="Welcomemessages:", value = 'You can use ModNPC to send welcomemessages when a member joins. The command for that is `!setwelcomemessage "link to the channel where the welcomemessage will be posted" "link to message with the content")` Be aware that this function is not programmed completly. This means you can not mention the new member or show stats of your server.', inline = False)
    await ctx.reply(embed=embed)