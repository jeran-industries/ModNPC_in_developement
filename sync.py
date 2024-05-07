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
            newnewembed = discord.Embed(title=f'Command update completed', description=f"Check it out: https://discordbotlist.com/bots/modnpc/commands", color=discord.Color.orange())
            await message.edit(embed = newnewembed)
            return()
    embed = discord.Embed(title=f'Attention', description=f"You aren't allowed to use this command!!!", color=discord.Color.dark_red())
    upload_commands(botlisttoken)
    await ctx.send(embed = embed)


def upload_commands(bot_token):
    bot_id = 1144006301765095484
    url = f"https://discordbotlist.com/api/bots/{bot_id}/commands"
    headers = {
        "Authorization": f"{bot_token}"
    }
    response = requests.post(url, headers=headers, json="commands.json")

async def reconnectcommand(bot):
    await bot.reconnect()

async def disconnectcommand(bot):
    await bot.disconnect()