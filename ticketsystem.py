import discord
from datetime import datetime


#own modules:
from sqlitehandler import get_opentickets_categoryid, get_closedtickets_categoryid, update_ticket_status, get_creatorid_ticket, get_ticketsystem_status, get_claimerid_ticket, insert_into_tickettable

class OpenTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open a Ticket", custom_id="openticketbutton", emoji="📨")
    async def openaticket(self, interaction: discord.Interaction, button: discord.ui.button):
        guild = interaction.guild
        member = interaction.user
        bot = interaction.client
        ticketsystem_status = await get_ticketsystem_status(bot=bot, guildid=guild.id)
        if ticketsystem_status == "True":

            await interaction.response.send_modal(WhyTicket())
        else:
            embed = discord.Embed(title="Hmm let me check", description=f"Your server team created this message but they didnt activated the ticketfeature.\nYou can try pinging them or writing them a dm.")
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)

class WhyTicket(discord.ui.Modal, title="More details for your ticket:"):
    Shortreason = discord.ui.TextInput(label="Why are you opening this ticket?", placeholder="For example: I want to report someone.", style=discord.TextStyle.short)
    Longtext = discord.ui.TextInput(label="What exactly happened?", placeholder="For example: He did this and i didnt like that.", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        member = interaction.user
        bot = interaction.client
        guild = interaction.guild
        channel = interaction.channel

        embed = discord.Embed(title="New ticket", description=f"{member.name} ||{member.id}|| opened a ticket")
        embed.add_field(name="Why are you opening this ticket?", value=self.Shortreason)
        embed.add_field(name="What exactly happened?", value=self.Longtext)
        embed.set_footer(text=f"{bot.user.name} | {datetime.utcnow()}")

        opentickets_categoryid = await get_opentickets_categoryid(bot=bot, guildid=guild.id)
        opentickets_category = guild.get_channel(opentickets_categoryid)
        channel = await opentickets_category.create_text_channel(name="Ticket")
        await channel.edit(name=f"Ticket-{channel.id}")
        await channel.set_permissions(target=guild.default_role, read_messages=False, send_messages=False)
        await channel.set_permissions(target=member, read_messages=True, send_messages=True)

        await channel.send(embed=embed, view=Unclaimedticketbuttons())

        await insert_into_tickettable(bot=bot, guildid=guild.id, channelid=channel.id, creatorid=member.id) #channelid = ticketid

        embed = discord.Embed(title="Ticket was created", description=f"Your ticket was created in {channel.mention}")
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=60)

class Unclaimedticketbuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", custom_id="claimticketbutton", emoji="🎫", disabled=False)
    async def claimaticket(self, interaction: discord.Interaction, button: discord.ui.button):
        channel = interaction.channel
        member = interaction.user
        bot = interaction.client
        guild = interaction.guild
        creatorid = await get_creatorid_ticket(bot=bot, ticketid=interaction.channel.id)
        if creatorid == member.id or creatorid == 945785058676072448:
            embed = discord.Embed(title="You can't claim the ticket you issued")
            await interaction.response.send_message(embed=embed)
        else:
            await update_ticket_status(bot=bot, ticketid=channel.id, status=1, claimerid=member.id)
            embed = discord.Embed(title="Someone claimed the ticket", description = f"{member.mention} claimed the ticket <#{channel.id}>, <@{creatorid}> issued")
            await interaction.response.send_message(embed=embed)
    
    @discord.ui.button(label="Close", custom_id="closeticketbutton", emoji="🔒", disabled=False)
    async def closeaticket(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild
        await interaction.response.defer(thinking=True)
        #ticketid = messageid ticketstatus = 0(unclaimed) 1(claimed) 2(closed) 3(reopened&unclaimed) 4(reopened&claimed)
        await update_ticket_status(bot=bot, ticketid=channel.id, status=2, claimerid=member.id)

        closedtickets_categoryid = await get_closedtickets_categoryid(bot=bot, guildid=guild.id)
        closedtickets_category = guild.get_channel(closedtickets_categoryid)

        creatorid = await get_creatorid_ticket(bot=bot, ticketid=channel.id)
        creator = guild.get_member(creatorid)

        await channel.edit(category = closedtickets_category)
        await channel.set_permissions(target=creator, read_messages=False, send_messages=False)

        embed = discord.Embed(title="The ticket got closed", description = f"The ticket from <@{creatorid}> <#{channel.id}> got closed by {member.mention}")
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Reopen", custom_id="reopenticketbutton", emoji="🔓", disabled=False)
    async def reopenaticket(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        guild = interaction.guild
        channel = interaction.channel
        member = interaction.user
        await interaction.response.defer(thinking=True)
        #ticketid = messageid ticketstatus = 0(unclaimed) 1(claimed) 2(closed) 3(reopened&unclaimed) 4(reopened&claimed)
        ticketsystem_status = await get_ticketsystem_status(bot=bot, guildid=guild.id)
        creatorid = await get_creatorid_ticket(bot=bot, ticketid=channel.id)
        creator = guild.get_member(creatorid)
        if ticketsystem_status == 1:
            await update_ticket_status(bot=bot, ticketid=channel.id, status=4, claimerid=member.id)
            claimerid = await get_claimerid_ticket(bot=bot, ticketid=channel.id)
            embed = discord.Embed(title=f"The ticket was reopened.")
            await interaction.followup.send(content=f"<@{creatorid}> <@{claimerid}", embed = embed)
        else:
            await update_ticket_status(bot=bot, ticketid=channel.id, status=3, claimerid=member.id)
            embed = discord.Embed(title=f"The ticket was reopened.")
            await interaction.followup.send(content=f"<@{creatorid}>", embed = embed)

        openedtickets_categoryid = await get_opentickets_categoryid(bot=bot, guildid=guild.id)
        openedtickets_category = guild.get_channel(openedtickets_categoryid)
            
        await channel.edit(category = openedtickets_category)
        await channel.set_permissions(target=creator, read_messages=True, send_messages=True)