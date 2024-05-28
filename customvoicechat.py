class customvoicechatcontrolmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Test", custom_id="test")
    async def test(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")