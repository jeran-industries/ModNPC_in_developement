import discord

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