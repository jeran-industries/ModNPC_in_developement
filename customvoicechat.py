#database:
#table guild: guildid ... j2createchannelid

#table customvoicechats: guildid, ownerid, name, status (locked/unlocked/hided), limit, password

#table permitted_people: guildid, ownerid, memberid

#table blocked_people: ownerid, memberid

#table mods: guildid, ownerid, memberid

#commands:
#/cvc_join_request: if accepted by mods or owner permits person and adds person to currentcvcpermittedpeopletable
#/cvc_claim: changes the channel to the customvoicechat if it exists if not: already existing channel gets added to database, only if owner or mods arent there anymore, changes ownerid of currentcvctable
#/cvc_rename: renames the cvc if user is mod or owner, changes currentcvctable
#/cvc_limit: changes the limit of the vc if user is mod or owner, changes currentcvctable
#/cvc_permit: permit a person by their memberid or selectmenu if user is mod or owner to currentcvcpermittedpeopletable
#/cvc_unpermit: unpermits a person by their memberid or selectmenu if user is mod or owner from cvcpermittedpeopletable
#/cvc_block: blocks a person by their memberid or selectmenu out of own cvc and if user is mod out of the owners cvc
#/cvc_unblock: unblocks a person by their memberid or selectmenu out of own cvc and if user is mod out of the owners cvc
#/cvc_hide: hides the channel from all users and saves to currentcvctable
#/cvc_unhide: unhides the channel from all users and saves to currentcvctable
#/cvc_addmod: adds a mod if user is owner
#/cvc_removemod: removes a mod if user is owner
#/cvc_activaterecordmode: activate recording mode if user is owner or mod
#/cvc_deactivaterecordmode: deactivate recording mode if user is owner or mod
#/cvc_savesession: adds permitted people from currentcvcpermittedpeopletable to cvcpermittedpeopletable, 

import discord
import builtins

#own modules:
from sqlitehandler import check4jointocreatechannel, check4savedcvc, check4currentcvc, get_cvc, get_current_cvc, get_current_cvcs, get_mods, add_mod, remove_mod, insert_cvc, insert_into_current_cvctable, get_permitted_member, get_current_permitted_member, delete_current_cvc, rename_current_cvc, limit_current_cvc, add_current_permitted_user, add_permitted_user, delete_current_permits, update_cvc

async def cvc(bot, member, beforechannel, afterchannel):
    if beforechannel is not None:
        await check4emptycvc(bot=bot, member=member, channel=beforechannel)

    if afterchannel is not None:
        await jointocreate(bot=bot, member=member, channel=afterchannel)
        
async def check4emptycvc(bot, member, channel):
    if len(channel.members) == 0 and await check4currentcvc(bot=bot, guildid=member.guild.id, ownerid=member.id, channelid=channel.id) is True:
        await channel.delete(reason = "Deleting a custom voicechannel because it is empty.")
        await delete_current_cvc(bot=bot, channelid=channel.id)
        await delete_current_permits(bot=bot, channelid=channel.id)

async def jointocreate(bot, member, channel):
    guild=member.guild
    if channel is not None and await check4jointocreatechannel(bot=bot, guildid=guild.id, channelid=channel.id) is True: #check if member joins a channel and if the joined channel is the jointocreate channel (j2c)
        j2cchannel=channel
        if await check4savedcvc(bot=bot, guildid=guild.id, ownerid=member.id) is True:
            name, status, vclimit, password = await get_cvc(bot=bot, guildid=guild.id, ownerid=member.id)
            permitted_memberids = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=member.id)
            print(name, status, vclimit, password)

        else:
            await insert_cvc(bot=bot, guildid=guild.id, ownerid=member.id, name=member.display_name)

            name = f"CVC from {member.display_name}"
            status = 0
            vclimit = 0
            password = None

        print(name, status, vclimit, password)

        cvccategory = j2cchannel.category
        cvc = await cvccategory.create_voice_channel(name=name, reason="Creating a custom voicechannel", user_limit=vclimit, position=1)
        await member.move_to(channel = cvc, reason = "Moving member from Join to create channel to the custom voicechannel")
        await insert_into_current_cvctable(bot=bot, guildid=guild.id, ownerid=member.id, channelid=cvc.id, name=name, status=status, vclimit=vclimit, password=password)
        for permitted_memberid in permitted_memberids:
            await add_current_permitted_user(bot=bot, guildid=guild.id, ownerid=member.id, channelid=cvc.id, memberid=permitted_memberid)
        message = await cvc.send(view=customvoicechatcontrolmenu())
        #await message.pin()
    else:
        print("Im here ig")

async def regularcheck4emptycvc(bot):
    current_cvcs = await get_current_cvcs(bot=bot)
    for guild in bot.guilds:
        for voicechannel in guild.voice_channels:
            if len(voicechannel.members) == 0:
                if voicechannel.id in current_cvcs:
                    await voicechannel.delete(reason = "Deleting a custom voicechannel because it is empty.")
                    print("Deleted empty voicechannel in the regular check")
                

class customvoicechatcontrolmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Rename", custom_id="renamecustomvoicechat")
    async def rename(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(RenameModal())
    
    @discord.ui.button(label="Limit", custom_id="limitcustomvoicechat")
    async def limit(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(LimitModal())

    @discord.ui.button(label="CVC info", custom_id="listmodscustomvoicechat")
    async def cvcinfo(self, interaction: discord.Interaction, button: discord.ui.button):
        bot=interaction.client
        guild=interaction.guild
        channel=interaction.channel

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        if vclimit == 0:
            vclimit = "-"
        embed = discord.Embed(title="CVC Infos", description=f"name: {name}\nowner: <@{ownerid}>\nvclimit: `{vclimit}`")

        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)
        modsmention = ""
        for modid in modids:
            modsmention = f"<@{modid}>\n" + modsmention
        embed.add_field(name="Mods",value=modsmention, inline=False)

        currentpermittedmemberids = await get_current_permitted_member(bot=bot, channelid=channel.id)
        currentpermittedmention = ""
        for currentpermittedmemberid in currentpermittedmemberids:
            currentpermittedmention = f"<@{currentpermittedmemberid}>\n" + currentpermittedmention
        embed.add_field(name="Current permitted members",value=currentpermittedmention, inline=False)

        permittedmemberids = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=ownerid)
        permittedmention = ""
        for permittedmemberid in permittedmemberids:
            permittedmention = f"<@{permittedmemberid}>\n" + permittedmention
        embed.add_field(name="Permitted members",value=permittedmention, inline=False)

        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Hide", custom_id="hidecustomvoicechat")
    async def hide(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")

    @discord.ui.button(label="Unhide", custom_id="unhidecustomvoicechat")
    async def unhide(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")

    @discord.ui.button(label="Permit", custom_id="permitcustomvoicechat")
    async def permit(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=PermitSelect())

    @discord.ui.button(label="Unpermit", custom_id="unpermitcustomvoicechat")
    async def unpermit(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")

    @discord.ui.button(label="Block", custom_id="blockcustomvoicechat")
    async def block(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")

    @discord.ui.button(label="Unblock", custom_id="unblockcustomvoicechat")
    async def unblock(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")

    @discord.ui.button(label="Add mod", custom_id="addmodcustomvoicechat")
    async def addmod(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=AddModSelect())

    @discord.ui.button(label="Remove mod", custom_id="removemodcustomvoicechat")
    async def removemod(self, interaction: discord.Interaction, button: discord.ui.button):
        bot=interaction.client
        guild=interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=interaction.channel.id)
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)

        options=[]
        for modid in modids:
            mod = guild.get_member(modid)
            options.append(f"discord.SelectOption(label={mod.display_name}, description={mod.name})")

        labellist = []
        for modid in modids:
            mod = guild.get_member(modid)
            #levelrole = discord.utils.get(guild.roles, id=levelroleid)
            labellist.append(discord.SelectOption(label=mod.display_name, description=mod.name, value=mod.id),)
            print(labellist)
        
        if modids == []:
            placeholder="You dont have any mods"
            labellist = [discord.SelectOption(label="No mods", value=0)]
            status=True
        else:
            placeholder="Select a mod you want to be removed"
            status=False
        await interaction.response.send_message(view=RemoveModSelect(options=labellist, placeholder=placeholder, status=status))
    
    @discord.ui.button(label="Set Password", custom_id="setpasswordcustomvoicechat")
    async def setpassword(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")
    
    @discord.ui.button(label="Save Session", custom_id="savesessioncustomvoicechat")
    async def savesession(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        if member.id == ownerid:
            current_permitted_memberids = await get_current_permitted_member(bot=bot, channelid=channel.id)
            permitted_memberids = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=ownerid)
            for current_permitted_memberid in current_permitted_memberids:
                if current_permitted_memberid in permitted_memberids:
                    pass
                else:
                    await add_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=current_permitted_memberid)
            await update_cvc(bot=bot, guildid=guild.id, ownerid=ownerid, name=name, status=status, vclimit=vclimit, password=password)
            embed = discord.Embed(title="Success", description="You saved the settings")
        else:
            embed = discord.Embed(title="Error", description="Only the owner can save the settings")
        await interaction.response.send_message(embed=embed)
        

class RenameModal(discord.ui.Modal, title="How should your custom voicechat be called"):
    name = discord.ui.TextInput(label="Enter the channel's new name", placeholder="Enter the channel's new name", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        name = str(self.name)
        successembed = discord.Embed(title="Success", description=f"You renamed the channel to `{name}`.")
        try:
            if member.id == ownerid:
                await channel.edit(name=name)
                await rename_current_cvc(bot=bot, channelid=channel.id, name=name)
                await interaction.response.send_message(embed=successembed)
            elif member.id in (await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)):
                await channel.edit(name=name)
                await rename_current_cvc(bot=bot, channelid=channel.id, name=name)
                await interaction.response.send_message(embed=successembed)
            else:
                errorembed = discord.Embed(title="Error", description=f"You cant rename the channel because you arent the owner or a mod of the channel.")
                await interaction.response.send_message(embed=errorembed, ephemeral=True)
        except Exception as error:
            #await bot.discorderrorlog(error)

            errorembed = discord.Embed(title="Hmm Something went wrong", description=f"Hmm Something went wrong: \n`{type(error)}: {error}`")
            await interaction.response.send_message(embed=errorembed, ephemeral=True)

class LimitModal(discord.ui.Modal, title="How many people can join the channel?"):
    limit = discord.ui.TextInput(label="Limit the channel", placeholder="Enter a number between 1 and 99 or something else", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)

        try:
            if member.id == ownerid or member.id in await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid):
                vclimit = str(self.limit)
                vclimit = int(vclimit)
                if vclimit in list(builtins.range(1, 100)):
                    successembed = discord.Embed(title="Success", description=f"You limited the channel to `{vclimit}`.")
                else:
                    vclimit = 0
                    successembed = discord.Embed(title="Success", description=f"You unlimited the channel.")

                print(channel.name)
                await channel.edit(user_limit=vclimit, reason=f"Limiting a custom voicechannel from {ownerid} by {member.id}")

                await limit_current_cvc(bot=bot, channelid=channel.id, vclimit=vclimit)
                
                await interaction.response.send_message(embed=successembed)
            else:
                errorembed = discord.Embed(title="Error", description=f"You can't limit the channel because you aren't the owner or a mod of the channel.")
                await interaction.response.send_message(embed=errorembed, ephemeral=True)
        except Exception as error:
            #await bot.discorderrorlog(error=error)

            errorembed = discord.Embed(title="Hmm Something went wrong", description=f"Hmm Something went wrong")
            await interaction.response.send_message(embed=errorembed, ephemeral=True)

class PermitSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PermitSelectMenu())

class PermitSelectMenu(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the member to permit")

    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        guild = interaction.guild
        member = self.values[0]
        channel = interaction.channel
        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)
        currentpermittedmembers = await get_current_permitted_member(bot=bot, channelid=channel.id)
        permittedmembers = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=ownerid)

        if member.id == ownerid or member.id in modids:
            if member.id in currentpermittedmembers:
                embed = discord.Embed(title="Error", description="You already permitted this person.")
            elif member.id in permittedmembers:
                embed = discord.Embed(title="Error", description="You already permitted this person.")
            else:
                embed = discord.Embed(title="Success", description=f"You permitted {member.mention}.")
                await add_current_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, channelid=channel.id, memberid=member.id)
        else:
            embed = discord.Embed(title="Error", description="You aren't the owner or a mod of this channel.")
        
        await interaction.response.send_message(embed=embed)

class AddModSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(AddModSelectMenu())

class AddModSelectMenu(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the member to add as a mod")

    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        guild = interaction.guild
        member = interaction.user
        channel = interaction.channel
        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        mods = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)
        if member.id == ownerid:
            if self.values[0].id in mods:
                embed = discord.Embed(title="Success", description=f"You already added {self.values[0].mention} as a mod.")
            elif len(mods) < 26:
                await add_mod(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=self.values[0].id)
                embed = discord.Embed(title="Success", description=f"You added {self.values[0].mention} as a mod.")
            else:
                embed = discord.Embed(title="Error", description="You cant have more than 25 mods.")
        else:
            embed = discord.Embed(title="Error", description="You aren't the owner of this channel.")
        await interaction.response.send_message(embed=embed)

class RemoveModSelect(discord.ui.View):
    def __init__(self, options, placeholder, status):
        super().__init__()
        self.add_item(RemoveModSelectMenu(options = options, placeholder=placeholder, status = status))

class RemoveModSelectMenu(discord.ui.Select):
    def __init__(self, options, placeholder, status):
        super().__init__(placeholder=placeholder, options=options, disabled=status)

    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        guild = interaction.guild
        member = interaction.user
        channel = interaction.channel
        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        if member.id == ownerid:
            await remove_mod(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=self.values[0])
            embed = discord.Embed(title="Success", description=f"You added {self.values[0]} as a mod.")
        else:
            embed = discord.Embed(title="Error", description="You aren't the owner of this channel.")
        await interaction.response.send_message(embed=embed)