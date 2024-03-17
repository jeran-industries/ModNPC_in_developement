from random import randint
import discord

#command: !throwadice 'how many sides' 'how many dices'
async def throwdicecommand(interaction, sides, dices):
    embed = discord.Embed(title='I threw a dice for you', description=f'You wanted {dices} dice with {sides} sides', color=discord.Color.dark_grey())
    i = 0
    while i < int(dices):  
        i = i + 1
        embed.add_field(name=f"The dice {i} is:", value=randint(1, int(sides)), inline=False)     
    #await ctx.delete()
    await interaction.response.send_message(embed = embed)