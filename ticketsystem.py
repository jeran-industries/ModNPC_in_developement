import discord

class OpenTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open a Ticket", custom_id="openticketbutton")
    async def openaticket(self, interaction: discord.Interaction, button: discord.ui.button):
        guild = interaction.guild
        await guild.create_text_channel()
        await interaction.response.send_message()