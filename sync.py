import discord
import requests

#Syncing all slashcommands
async def synccommand(ctx, bot, botlisttoken): #only 4 Member of developerteam
    member = ctx.author
    permitteduser = [945785058676072448]
    for i in permitteduser:
        if member.id == i:
            embed = discord.Embed(title=f'Syncing commands...', description=f"Syncing commands...", color=discord.Color.orange())
            message = await ctx.reply(embed = embed)
            await bot.tree.sync()
            newembed = discord.Embed(title=f'Syncing commands completed', description=f"Syncing commands completed, running command update on https://discordbotlist.com/bots/modnpc/commands", color=discord.Color.orange())
            await message.edit(embed = newembed)
            return()
    embed = discord.Embed(title=f'Attention', description=f"You aren't allowed to use this command!!!", color=discord.Color.dark_red())
    upload_commands(botlisttoken)
    await ctx.reply(embed = embed)


def upload_commands(bot_token):
    bot_id = 1144006301765095484
    url = f"https://discordbotlist.com/api/bots/{bot_id}/commands"
    headers = {
        "Authorization": f"{bot_token}"
    }
    commands =  [
                    {
                        "name": "status",
                        "description": "You can check the status of the bot out.",
                        "type": 1
                    },
                    {
                        "name": "patreon",
                        "description": "You can check some funny stuff about this bot out and support us.",
                        "type": 1
                    },
                    {
                        "name": "setup",
                        "description": "Probably the most important command of this bot. With it you can activate, deactivate and do much more for setup.",
                        "type": 1
                    },
                    {
                        "name": "create_reactionrole",
                        "description": "With this command you can create a message to which you can append reactionroles.",
                        "type": 1
                    },
                    {
                        "name": "add_reactionrole",
                        "description": "With this command you can append to a created reactionrole message new reactionroles.",
                        "type": 1
                    },
                    {
                        "name": "polls",
                        "description": "With this command you can create a poll.",
                        "type": 1
                    },
                    {
                        "name": "throwadice",
                        "description": "With this command you can throw dices. You can decide how much dices you throw and how much sides the dices have-",
                        "type": 1
                    },
                    {
                        "name": "rank",
                        "description": "With this command you can look up your stats on a server.",
                        "type": 1
                    },
                    {
                        "name": "addxp",
                        "description": "With this command you can add xp to a user.",
                        "type": 1
                    },
                    {
                        "name": "removexp",
                        "description": "With this command you can remove xp from a user.",
                        "type": 1
                    },
                    {
                        "name": "leaderboard",
                        "description": "With this command you can look the leaderboard of your server up.",
                        "type": 1
                    },
                    {
                        "name": "claim",
                        "description": "With this command you can get xp by upvoting the bot on discordbotlist. After upvoting, run this command again to get your promised xp on the server",
                        "type": 1
                    }           
                ]
    response = requests.post(url, headers=headers, json=commands)
    print(response.status_code)