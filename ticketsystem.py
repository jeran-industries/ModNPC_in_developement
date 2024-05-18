import discord

#own modules:
from sqlitehandler import get_opentickets_categoryid, get_closedtickets_categoryid

class OpenTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open a Ticket", custom_id="openticketbutton", emoji="📨")
    async def openaticket(self, interaction: discord.Interaction, button: discord.ui.button):
        guild = interaction.guild
        bot = interaction.client
        opentickets_categoryid = await get_opentickets_categoryid(bot=bot, guildid=guild.id)
        

        await opentickets_category.create_text_channel(name="test")
        