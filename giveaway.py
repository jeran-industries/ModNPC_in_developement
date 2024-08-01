#timelimit: command
#prize: command
#how many prizes: command
#role: command, optional
#color: command, optional
#description: modal, optional

#buttons before giveaway is closed:
#Join Giveaway
#Close Giveaway
#Extend Giveaway (optional)

#buttons after giveaway is closed:
#Reroll Giveaway

#db:
#giveawaytable: guildid, hostid, messageid, prize, roleid, time2close
#giveawayparticipantstable: guildid, messageid, memberid

import discord
import builtins
from math import floor
import datetime
import random

#own modules
from sqlitehandler import add_giveaway, check_4_user_in_giveaway, add_user_2_giveaway, remove_user_from_giveaway, get_all_giveaways_by_time, delete_giveaway, get_participants_by_giveawayid, get_giveaway, remove_users_from_giveaway

async def check4closinggiveaways(bot):
    currenttime=int(round((datetime.datetime.now(datetime.timezone.utc) - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()))
    guildids, guildchannelids, giveawaymessageids = await get_all_giveaways_by_time(bot=bot, time=currenttime)
    #print(guildchannelids)
    #print(giveawaymessageids)
    #giveawaymessageids = None
    if giveawaymessageids is not None:
        i=0
        for giveawaymessageid in giveawaymessageids:
            guild = bot.get_guild(guildids[i])
            if guild is None:
                print("Couldnt get guild")
                return
            print(guild.text_channels)
            print(guildchannelids[i])
            channel = guild.get_channel(guildchannelids[i]) #getting the channel from the message
            if channel is None:
                print("Couldnt get channel")
                return
            giveawaymessage = await channel.fetch_message(giveawaymessageid) #getting the message to add a reaction so the user can more easy react 
            if giveawaymessage is not None:
                giveawaymessageembed = giveawaymessage.embeds[0]
                giveawaymessageembed.set_field_at(index=1, name = "Closed", value = giveawaymessageembed.fields[1].value, inline = True)
                await giveawaymessage.edit(embed=giveawaymessageembed, view=None)
                await selectwinner_giveaway(bot=bot, guild=guild, channel=channel, messageid=giveawaymessageid)
                await delete_giveaway(bot=bot, messageid=giveawaymessage.id)
            else:
                print("Couldnt fetch message")
            i = i + 1

async def giveaway_list_command(interaction):
    pass

async def giveaway_add_command(interaction, prize, number_of_prizes, role, timelimit, mention, color):
    #check if user is allowed to do giveaways
    if interaction.user.guild_permissions.administrator is False:
        embed = discord.Embed(title="Error", description="You cant start a giveaway because you arent an adminstrator.", colour=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    currenttime=int(round((datetime.datetime.now(datetime.timezone.utc) - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()))
    time = currenttime + timelimit
    if currenttime >= time:
        embed = discord.Embed(title="Error", description="You cant set the timer for the giveaway to under one minute.", colour=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if number_of_prizes not in builtins.range(1, 25):
        embed = discord.Embed(title="Error", description="You can only set the number of prizes between 1 and 25. 1 is default.", colour=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return 

    if color == "blue":
        color = discord.Color.blue()
    elif color == "blurple":
        color = discord.Color.blurple()
    elif color == "gold":
        color = discord.Color.gold()
    elif color == "green":
        color = discord.Color.green()
    elif color == "magenta":
        color = discord.Color.magenta()
    elif color == "orange":
        color = discord.Color.orange()
    elif color == "pink":
        color = discord.Color.pink()
    elif color == "purple":
        color = discord.Color.purple()
    elif color == "random":
        color = discord.Color.random()
    elif color == "red":
        color = discord.Color.red()
    elif color == "yellow":
        color = discord.Color.yellow()

    #only for test purposes
    await interaction.response.send_modal(Giveaway_Modal(prize=prize, number_of_prizes=number_of_prizes, role=role, timelimit=timelimit, mention=mention, color=color))

class Giveaway_Modal(discord.ui.Modal, title="Enter the giveaway description"):
    def __init__(self, prize, number_of_prizes, role, timelimit, mention, color):
        self.prize = prize
        self.number_of_prizes = number_of_prizes
        self.role = role
        self.timelimit = timelimit
        self.mentionstatus = mention
        self.color = color
        super().__init__()

    description = discord.ui.TextInput(label="Enter the giveaway description", style=discord.TextStyle.long, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        number_of_prizes = self.number_of_prizes
        print(self.role)
        if self.role is None:
            embed = discord.Embed(title=f"{interaction.user.display_name} gives {self.number_of_prizes} {self.prize} away.", description=self.description, colour=self.color)
            mention = interaction.guild.default_role
        else:
            embed = discord.Embed(title=f"{interaction.user.display_name} gives {self.number_of_prizes} {self.prize} to {self.role.mention} away.", description=self.description, colour=self.color)
            mention = self.role.mention
        embed.add_field(name="Number of Participants:", value=0)
        embed.add_field(name="Closes:", value=f"<t:{int(round((datetime.datetime.now(datetime.timezone.utc) - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds())) + self.timelimit}:R>")
        if self.mentionstatus == "Yes":
            await interaction.response.send_message(content=mention, embed=embed, ephemeral=True, view=giveaway_verifytestbuttons_view(prize = self.prize, number_of_prizes = self.number_of_prizes, role=self.role, timelimit=self.timelimit, mention=self.mentionstatus, color=self.color, description=self.description))
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True, view=giveaway_verifytestbuttons_view(prize = self.prize, number_of_prizes = self.number_of_prizes, role=self.role, timelimit=self.timelimit, mention=self.mentionstatus, color=self.color, description=self.description))

class giveaway_verifytestbuttons_view(discord.ui.View):
    def __init__(self, prize, number_of_prizes, role, timelimit, color, mention, description):
        self.prize = prize
        self.number_of_prizes = number_of_prizes
        self.role = role
        self.timelimit = timelimit
        self.mentionstatus = mention
        self.color = color
        self.description = description
        super().__init__(timeout=None)

    @discord.ui.button(label="Join", custom_id="joingiveawaypreview", row=0, disabled=True)
    async def joingiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title="This is just a preview, so this button rn doesnt work.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Close", custom_id="closegiveawaypreview", row=0, disabled=True)
    async def closegiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title="This is just a preview, so this button rn doesnt work.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Extend Giveaway", custom_id="extendgiveawaypreview", row=0, disabled=True)
    async def extendgiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button, disabled=True):
        embed=discord.Embed(title="This is just a preview, so this button rn doesnt work.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Create", custom_id="creategiveawaypreview", row=1)
    async def sendgiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.role is None:
            embed = discord.Embed(title=f"{interaction.user.display_name} gives {self.number_of_prizes} {self.prize} away.", description=self.description, colour=self.color)
            mention = interaction.guild.default_role
        else:
            embed = discord.Embed(title=f"{interaction.user.display_name} gives {self.number_of_prizes} {self.prize} to {self.role.mention} away.", description=self.description, colour=self.color)
            mention = self.role.mention
        time2close = int(round((datetime.datetime.now(datetime.timezone.utc) - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds())) + self.timelimit
        embed.add_field(name="Number of Participants:", value=0)
        embed.add_field(name="Closes:", value=f"<t:{time2close}:R>")
        #yes -> save to db and send 
        await interaction.response.send_message(content=".", delete_after=0.1)
        message = await interaction.channel.send(embed=embed)
        await message.edit(view=giveaway_buttons_view(timeout=self.timelimit, message=message))
        bot = interaction.client
        if self.role is None:
            await add_giveaway(bot=bot, guildid=interaction.guild.id, hostid=interaction.user.id, channelid=interaction.channel.id, messageid=message.id, prize=self.prize, numberofprizes=self.number_of_prizes, roleid=None, time2close=time2close)
        else:
            await add_giveaway(bot=bot, guildid=interaction.guild.id, hostid=interaction.user.id, channelid=interaction.channel.id, messageid=message.id, prize=self.prize, numberofprizes=self.number_of_prizes, roleid=self.role.id, time2close=time2close)

    @discord.ui.button(label="Discard", custom_id="discardgiveawaypreview", row=1)
    async def discardgiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title="You discarded this giveaway.")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    #Do you verify?

class giveaway_buttons_view(discord.ui.View):
    def __init__(self, timeout=None, message=None):
        self.message = message
        super().__init__(timeout=None)

    @discord.ui.button(label="Join", custom_id="joingiveawaypreview")
    async def joingiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button, row=0):
        bot=interaction.client
        message=interaction.message
        member=interaction.user
        guild=interaction.guild

        guildid, channelid, hostid, messageid, prize, number_of_prizes, roleid, time2close = await get_giveaway(bot=bot, messageid=message.id)

        if roleid is not None:
            roleids = []
            roles = member.roles
            for role in roles:
                roleids.append(role.id)
        
            if roleid in roleids:
                pass
            else:
                embed = discord.Embed(title="You aren't allowed to participate in this giveaway.", description=f"You need to have <@{roleid}> to enter this giveaway")
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 20)
                return
        
        if await check_4_user_in_giveaway(bot=bot, messageid=message.id, memberid=member.id) is False:
            embed = discord.Embed(title="You entered successfully the giveaway")
            await add_user_2_giveaway(bot=bot, guildid=guild.id, messageid=message.id, memberid=member.id)
            messageembed = message.embeds[0]
            messageembed.set_field_at(index=0, name = messageembed.fields[0].name, value = int(messageembed.fields[0].value) + 1, inline = True)
            await message.edit(embed=messageembed)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 10)
        else:
            embed = discord.Embed(title="You are already in the giveaway.", description="You can leave the giveaway if you want to.")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 20, view=leavegiveaway_button_view(message))
        #check if user is allowed to take part
        #True: check if user already entered the giveaway
            #True: save user to giveawayparticipantstable -> make counter once bigger
            #False: error
        #False: error

    @discord.ui.button(label="Close", custom_id="closegiveawaypreview")
    async def closegiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button, row=0):
        bot = interaction.client
        guild = interaction.guild
        channel = interaction.channel
        giveawaymessage = interaction.message
        await selectwinner_giveaway(bot=bot, guild=guild, channel=channel, messageid=giveawaymessage.id)
        await remove_users_from_giveaway(bot=bot, messageid=giveawaymessage.id)
        messageembed = giveawaymessage.embeds[0]
        messageembed.set_field_at(index = 1, name="Closed:", value=f"<t:{int(round((datetime.datetime.now(datetime.timezone.utc) - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()))}:R>")
        await giveawaymessage.edit(embed=messageembed, view=None)
        await delete_giveaway(bot=bot, messageid=giveawaymessage.id)
        await interaction.response.send_message(content=".", delete_after=0.01, ephemeral=True)

    @discord.ui.button(label="Extend Giveaway", custom_id="extendgiveawaypreview")
    async def extendgiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button, row=0):
        embed=discord.Embed(title="This is just a preview of this feature, so this button rn doesnt work.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class leavegiveaway_button_view(discord.ui.View):
    def __init__(self, message):
        self.message = message
        super().__init__(timeout=None)

    @discord.ui.button(label="Leave Giveaway", custom_id="leavegiveawaypreview")
    async def leavegiveawayscript(self, interaction: discord.Interaction, button: discord.ui.button, row=0):
        message=self.message
        bot=interaction.client
        member=interaction.user

        await remove_user_from_giveaway(bot=bot, messageid=message.id, memberid=member.id)
        embed = discord.Embed(title="You left the giveaway.")
        print(message.id)
        messageembed = message.embeds[0]
        messageembed.set_field_at(index=0, name = messageembed.fields[0].name, value = int(messageembed.fields[0].value) - 1, inline = True)
        await message.edit(embed=messageembed)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 10)

async def selectwinner_giveaway(bot, guild, channel, messageid):
    memberids = await get_participants_by_giveawayid(bot=bot, messageid=messageid)
    guildid, channelid, hostid, messageid, prize, number_of_prizes, roleid, time2close = await get_giveaway(bot=bot, messageid=messageid)
    i = 0
    if memberids == []:
        embed = discord.Embed(title=f"Sadly nobody participated in your giveaway.")
        await channel.send(content=f"<@{hostid}>", embed=embed)
        return
    print(number_of_prizes)
    while i <= number_of_prizes:
        if memberids != []:
            memberid = random.choice(memberids)
            member = guild.get_member(memberid)
            embed = discord.Embed(title=f"{member.display_name} just won {prize}.")
            await remove_user_from_giveaway(bot=bot, messageid=messageid, memberid=memberid)
            memberids.remove(memberid)
            await channel.send(content=f"<@{hostid}> {member.mention}", embed=embed)
        else:
            return
        i = i + 1
