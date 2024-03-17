import discord

#Syncing all slashcommands
async def synccommand(ctx, bot): #only 4 Member of developerteam
    member = ctx.author
    permitteduser = [945785058676072448]
    for i in permitteduser:
        if member.id == i:
            embed = discord.Embed(title=f'Syncing commands...', description=f"Syncing commands...", color=discord.Color.orange())
            message = await ctx.reply(embed = embed)
            await bot.tree.sync()
            newembed = discord.Embed(title=f'Syncing commands completed', description=f"Syncing commands completed", color=discord.Color.orange())
            await message.edit(embed = newembed)
            return()
    embed = discord.Embed(title=f'Attention', description=f"You aren't allowed to use this command!!!", color=discord.Color.dark_red())
    await ctx.reply(embed = embed)