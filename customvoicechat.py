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
from sqlitehandler import check4jointocreatechannel, check4savedcvc, check4currentcvc, get_cvc, get_current_cvc, get_current_cvcs, get_mods, add_mod, remove_mod, insert_cvc, insert_into_current_cvctable, get_permitted_member, get_current_permitted_member, delete_current_cvc, rename_current_cvc, limit_current_cvc, add_current_permitted_user, add_permitted_user, delete_current_permits, update_cvc, get_blocked_member, get_cvc_where_member_blocked, get_current_cvc_by_ownerid, delete_current_permitted_user, add_blocked_person, remove_blocked_person, change_ownerid, remove_permitted_user, change_customvcstatus

async def cvc(bot, member, beforechannel, afterchannel):
    if beforechannel is not None:
        guild = beforechannel.guild
        if await check4emptycvc(bot=bot, member=member, channel=beforechannel) is False: #if a empty channel wasnt found -> 
            current_cvcid = await get_current_cvc_by_ownerid(bot=bot, guildid = guild.id, ownerid=member.id)
            if current_cvcid == beforechannel.id:
                await member.move_to(beforechannel)
            elif current_cvcid is None:
                pass
            else:
                cvc = guild.get_channel(current_cvcid)
                if cvc is not None:
                    await member.move_to(cvc)

    if afterchannel is not None:
        await jointocreate(bot=bot, member=member, channel=afterchannel)
        
async def check4emptycvc(bot, member, channel):
    if len(channel.members) == 0 and await check4currentcvc(bot=bot, guildid=member.guild.id, ownerid=member.id, channelid=channel.id) is True:
        try:
            await channel.delete(reason = "Deleting a custom voicechannel because it is empty.")
        except Exception as error:
            bot.discorderrorlog(error=error)
        await delete_current_cvc(bot=bot, channelid=channel.id)
        await delete_current_permits(bot=bot, channelid=channel.id)
        return(True)
    else:
        return(False)

async def on_guild_join_rewrite_cvc_permissions(bot, member):
    guild = member.guild
    ownerids = await get_cvc_where_member_blocked(bot=bot, guildid=guild.id, memberid=member.id)
    if ownerid != []:
        for ownerid in ownerids:
            channelid, name, status, vclimit, password = await get_current_cvc_by_ownerid(bot=bot, guildid=guild.id, ownerid=ownerid)
            channel = guild.get_channel(channelid)
            await channel.set_permissions(target=member, connect=False)

async def checkifuserisallowedtojoincvc(bot, member, channel):
    if channel is not None:
        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        guild=channel.guild
        blocked_memberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=ownerid)
        if member.id in blocked_memberids:
            await member.move_to(channel=None, reason=f"User is blocked by cvc owner ({ownerid}).")
            await channel.set_permissions(target=member, connect=False)

async def jointocreate(bot, member, channel):
    guild=member.guild
    if channel is not None and await check4jointocreatechannel(bot=bot, guildid=guild.id, channelid=channel.id) is True: #check if member joins a channel and if the joined channel is the jointocreate channel (j2c)
        j2cchannel=channel
        if await check4savedcvc(bot=bot, guildid=guild.id, ownerid=member.id) is True:
            name, status, vclimit, password = await get_cvc(bot=bot, guildid=guild.id, ownerid=member.id)
            permitted_memberids = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=member.id)
            blocked_memberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=member.id)
            print(name, status, vclimit, password)

        else:
            await insert_cvc(bot=bot, guildid=guild.id, ownerid=member.id, name=member.display_name)

            name = f"CVC from {member.display_name}"
            status = 0
            vclimit = 0
            password = None

            permitted_memberids=[]
            blocked_memberids=[]

        print(name, status, vclimit, password)

        cvccategory = j2cchannel.category

        cvc = await cvccategory.create_voice_channel(name=name, reason="Creating a custom voicechannel", user_limit=vclimit, position=1, overwrites=await overwriteperms(bot=bot, guild=guild, status=status, permittedmemberids=permitted_memberids, blockedmemberids=blocked_memberids))
        await member.move_to(channel = cvc, reason = "Moving member from Join to create channel to the custom voicechannel")
        await cvc.move(after=j2cchannel)
        await insert_into_current_cvctable(bot=bot, guildid=guild.id, ownerid=member.id, channelid=cvc.id, name=name, status=status, vclimit=vclimit, password=password)
        for permitted_memberid in permitted_memberids:
            await add_current_permitted_user(bot=bot, guildid=guild.id, ownerid=member.id, channelid=cvc.id, memberid=permitted_memberid)
        embed = discord.Embed(title="Custom Voicechat Dashboard")
        embed.add_field(name="✍️", value="Rename")
        embed.add_field(name="👥", value="Limit")
        embed.add_field(name="🔒", value="Lock")
        embed.add_field(name="🔓", value="Unlock")
        embed.add_field(name="🤫", value="Hide")
        embed.add_field(name="🫨", value="Unhide")
        embed.add_field(name="👤➕", value="Permit")
        embed.add_field(name="👤➖", value="Unpermit")
        embed.add_field(name="⛔➕", value="Block")
        embed.add_field(name="⛔➖", value="Unblock")
        embed.add_field(name="👮➕", value="Add mod")
        embed.add_field(name="👮➖", value="Remove mod")
        embed.add_field(name="🚪", value="Kick")
        embed.add_field(name="💡", value="Custom Voicechat Infos")
        embed.add_field(name="💾", value="Save Session")
        embed.add_field(name="🛄", value="Claim")
        embed.add_field(name="🔑", value="Set Password")

        message = await cvc.send(embed=embed, view=customvoicechatcontrolmenu())
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

async def overwriteperms(bot, guild, status, permittedmemberids, blockedmemberids):
#unlocked: 0, locked&unhidden: 1, locked&hidden: 2
    if status == 0:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
            connect=True,
            )
        }

    elif status == 1:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
            send_messages=False,
            connect=False,
            )
        }

        for permittedmemberid in permittedmemberids:
            permittedmember = guild.get_member(permittedmemberid)
            if permittedmember is not None:
                overwrite = {
                    permittedmember: discord.PermissionOverwrite(
                        connect=True,
                    )
                }
            overwrites.update(overwrite)
        
    elif status == 2:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
            view_channel=False,
            send_messages=False,
            connect=False,
            )
        }

        for permittedmemberid in permittedmemberids:
            permittedmember = guild.get_member(permittedmemberid)
            if permittedmember is not None:
                overwrite = {
                    permittedmember: discord.PermissionOverwrite(
                        connect=True,
                        view_channel=True,
                    )
                }
            overwrites.update(overwrite)

    for blockedmemberid in blockedmemberids:
        blockedmember = guild.get_member(blockedmemberid)
        if blockedmember is not None:
            overwrite = {
                blockedmember: discord.PermissionOverwrite(
                    connect=False,
                )
            }
            overwrites.update(overwrite)
    
    return(overwrites)

class customvoicechatcontrolmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✍️", custom_id="renamecustomvoicechat", row=0)
    async def rename(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(RenameModal())
    
    @discord.ui.button(label="👥", custom_id="limitcustomvoicechat", row=0)
    async def limit(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_modal(LimitModal())

    @discord.ui.button(label="🔒", custom_id="lockcustomvoicechat", row=0)
    async def lock(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        print(status)
        #unlocked: 0, locked&unhidden: 1, locked&hidden: 2
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)
        channelmembers = interaction.channel.members

        if member.id == ownerid or member.id in modids:
            if status != 1: #check if channel is alr locked or not
                status = 1
                current_permitted_memberids = await get_current_permitted_member(bot=bot, channelid=channel.id)
                blockedmemberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=ownerid)
                for channelmember in channelmembers:
                    await add_current_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, channelid=channel.id, memberid=channelmember.id)
                await change_customvcstatus(bot=bot, status=status, channelid=channel.id)
                await channel.edit(overwrites=await overwriteperms(bot=bot, guild=guild, status=status, permittedmemberids=current_permitted_memberids, blockedmemberids=blockedmemberids))
                embed = discord.Embed(title="Success", description=f"{member.mention} locked the channel.")
            else: #channel is alr locked
                embed = discord.Embed(title="Error", description=f"The channel is already unlocked")
        else:
            embed = discord.Embed(title="Error", description=f"You dont have the rights to lock this channel")
        
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="🔓", custom_id="unlockcustomvoicechat", row=0)
    async def unlock(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        print(status)
        #unlocked: 0, locked&unhidden: 1, locked&hidden: 2
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)

        if member.id == ownerid or member.id in modids:
            if status == 1: #check if channel is alr unlocked or not
                status = 0
                current_permitted_memberids = await get_current_permitted_member(bot=bot, channelid=channel.id)
                blockedmemberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=ownerid)
                await change_customvcstatus(bot=bot, status=status, channelid=channel.id)
                await channel.edit(overwrites=await overwriteperms(bot=bot, guild=guild, status=status, permittedmemberids=current_permitted_memberids, blockedmemberids=blockedmemberids))
                embed = discord.Embed(title="Success", description=f"{member.mention} unlocked the channel.")
            else: #channel is alr locked
                embed = discord.Embed(title="Error", description=f"The channel is already unlocked")
        else:
            embed = discord.Embed(title="Error", description=f"You dont have the rights to unlock this channel")
        
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="🤫", custom_id="hidecustomvoicechat", row=1)
    async def hide(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        #unlocked: 0, locked&unhidden: 1, locked&hidden: 2
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)

        if member.id == ownerid or member.id in modids:
            if status != 2: #check if channel is alr locked or not
                status = 2
                current_permitted_memberids = await get_current_permitted_member(bot=bot, channelid=channel.id)
                blockedmemberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=ownerid)
                await change_customvcstatus(bot=bot, status=status, channelid=channel.id)
                await channel.edit(overwrites=await overwriteperms(bot=bot, guild=guild, status=status, permittedmemberids=current_permitted_memberids, blockedmemberids=blockedmemberids))
                embed = discord.Embed(title="Success", description=f"{member.mention} hided the channel.")
            else: #channel is alr locked
                embed = discord.Embed(title="Error", description=f"The channel is already hidden")
        else:
            embed = discord.Embed(title="Error", description=f"You dont have the rights to hide this channel")
        
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="🫨", custom_id="unhidecustomvoicechat", row=1)
    async def unhide(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        #unlocked: 0, locked&unhidden: 1, locked&hidden: 2
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)

        if member.id == ownerid or member.id in modids:
            if status == 2: #check if channel is alr unlocked or not
                status = 1
                current_permitted_memberids = await get_current_permitted_member(bot=bot, channelid=channel.id)
                blockedmemberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=newownerid)
                await change_customvcstatus(bot=bot, status=status, channelid=channel.id)
                await channel.edit(overwrites=await overwriteperms(bot=bot, guild=guild, status=status, permittedmemberids=current_permitted_memberids, blockedmemberids=blockedmemberids))
                embed = discord.Embed(title="Success", description=f"{member.mention} unhided the channel.")
            else: #channel is alr locked
                embed = discord.Embed(title="Error", description=f"The channel is already unhidden")
        else:
            embed = discord.Embed(title="Error", description=f"You dont have the rights to unhide this channel")
        
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="👤➕", custom_id="permitcustomvoicechat", row=1)
    async def permit(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=PermitSelect(), ephemeral = True)

    @discord.ui.button(label="👤➖", custom_id="unpermitcustomvoicechat", row=1)
    async def unpermit(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=UnPermitSelect(), ephemeral = True)

    @discord.ui.button(label="⛔➕", custom_id="blockcustomvoicechat", row=2)
    async def block(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=BlockSelect(), ephemeral = True)

    @discord.ui.button(label="⛔➖", custom_id="unblockcustomvoicechat", row=2)
    async def unblock(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=UnBlockSelect(), ephemeral = True)

    @discord.ui.button(label="👮➕", custom_id="addmodcustomvoicechat", row=2)
    async def addmod(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=AddModSelect(), ephemeral = True)

    @discord.ui.button(label="👮➖", custom_id="removemodcustomvoicechat", row=2)
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
        await interaction.response.send_message(view=RemoveModSelect(options=labellist, placeholder=placeholder, status=status), ephemeral = True)
    
    @discord.ui.button(label="🚪", custom_id="kickcustomvoicechat", row=3)
    async def kick(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=KickSelect(), ephemeral = True)

    @discord.ui.button(label=" 💡 ", custom_id="listmodscustomvoicechat", row=3)
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

        blockedmemberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=ownerid)
        blockedmention = ""
        for blockedmemberid in blockedmemberids:
            blockedmention = f"<@{blockedmemberid}>\n" + blockedmention
        embed.add_field(name="Blocked members",value=blockedmention, inline=False)

        await interaction.response.send_message(embed=embed)
    
    @discord.ui.button(label="💾", custom_id="savesessioncustomvoicechat", row=3)
    async def savesession(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        member = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        if member.id == ownerid:
            current_permitted_memberids = await get_current_permitted_member(bot=bot, channelid=channel.id, ownerid=ownerid)
            permitted_memberids = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=ownerid)
            for current_permitted_memberid in current_permitted_memberids:
                if current_permitted_memberid in permitted_memberids:
                    pass
                else:
                    await add_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=current_permitted_memberid)
            for permitted_memberid in permitted_memberids:
                if permitted_memberid in current_permitted_memberids: #if yes it means pass, if not the person got unpermitted and it gets transferred
                    pass
                else:
                    await remove_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=permitted_memberid)
            await update_cvc(bot=bot, guildid=guild.id, ownerid=ownerid, name=name, status=status, vclimit=vclimit, password=password)
            embed = discord.Embed(title="Success", description="You saved the settings")
        else:
            embed = discord.Embed(title="Error", description="Only the owner can save the settings")
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="🛄", custom_id="claimcustomvoicechat", row=3)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.button):
        bot = interaction.client
        channel = interaction.channel
        user = interaction.user
        guild = interaction.guild

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)

        if user.id == ownerid:
            embed = discord.Embed(title="Error", description="You are alreading owning this channel")
        #elif #owner is in channel
        elif ownerid in channel.members.id:
            embed = discord.Embed(title="Error", description="The owner is in the channel.")
        else:
            existing_mod=False
            for modid in modids:
                if modid in channel.members.id:
                    embed = discord.Embed(title="Error", description="A mod assigned by the owner is in the channel.")
                    existing_mod=True
                    break
            if existing_mod is False:
                await change_ownerid(bot=bot, channelid=channel.id, ownerid=user.id)
                newownerid = user.id
                permitted_userids = get_permitted_member(bot=bot, guildid=guild.id, ownerid=newownerid)
                for permitted_memberid in permitted_memberids:
                    await add_current_permitted_user(bot=bot, guildid=guild.id, ownerid=member.id, channelid=cvc.id, memberid=permitted_memberid)

                current_permitted_memberids = await get_current_permitted_member(bot=bot, channelid=channel.id)
                blockedmemberids = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=newownerid)

                await channel.edit(overwrites=await overwriteperms(bot=bot, guild=guild, status=status, permittedmemberids=current_permitted_memberids, blockedmemberids=blockedmemberids))
                embed = discord.Embed(title="Success", description=f"{member.mention} claimed the channel.")

        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label=" 🔑 ", custom_id="setpasswordcustomvoicechat", row=4)
    async def setpassword(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")

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
        user = interaction.user
        channel = interaction.channel

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)
        currentpermittedmembers = await get_current_permitted_member(bot=bot, channelid=channel.id, ownerid=ownerid)
        permittedmembers = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=ownerid)

        if user.id == ownerid or user.id in modids: #user is the user of the command
            if member.id in currentpermittedmembers:
                embed = discord.Embed(title="Error", description="You already permitted this person.")
            #elif member.id in permittedmembers:
            #    embed = discord.Embed(title="Error", description="You already permitted this person.")
            else:
                embed = discord.Embed(title="Success", description=f"You permitted {member.mention}.")
                await add_current_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, channelid=channel.id, memberid=member.id)
                if status == 1: #locked
                    await channel.set_permissions(target=member, connect=True)
                elif status == 2:
                    await channel.set_permissions(target=member, connect=True, view_channel=True)
        else:
            embed = discord.Embed(title="Error", description="You aren't the owner or a mod of this channel.")
        
        await interaction.response.send_message(embed=embed)

class UnPermitSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PermitSelectMenu())

class UnPermitSelectMenu(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the member to unpermit")

    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        guild = interaction.guild
        member = self.values[0]
        user = interaction.user
        channel = user.voice.channel

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)
        currentpermittedmembers = await get_current_permitted_member(bot=bot, channelid=channel.id, ownerid=ownerid)
        permittedmembers = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=ownerid)

        if user.id == ownerid or user.id in modids:
            if member.id == ownerid:
                embed = discord.Embed(title="Error", description="You can't unpermit the owner.")
            elif member.id in modids:
                embed = discord.Embed(title="Error", description="You can't unpermit a mod. If you are the owner, you have to remove their mod status first.")
            elif member.id in currentpermittedmembers:
                await delete_current_permitted_user(bot=bot, channelid=channel.id, memberid=member.id)
                embed = discord.Embed(title="Success", description=f"You unpermitted {member.mention}.")
                if status != 0: #locked or hidden
                    await channel.set_permissions(member, overwrite=None)
            elif member.id in permittedmembers:
                embed = discord.Embed(title="Error", description="You have already unpermitted or never permitted this person.")
            else:
                embed = discord.Embed(title="Error", description="You have already unpermitted or never permitted this person.")
        else:
            embed = discord.Embed(title="Error", description="You aren't the owner or a mod of this channel.")
        
        await interaction.response.send_message(embed=embed)

class BlockSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(BlockSelectMenu())

class BlockSelectMenu(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the member to block")

    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        guild = interaction.guild
        member = self.values[0]
        channel = interaction.channel
        user = interaction.user
        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        currentpermittedmembers = await get_current_permitted_member(bot=bot, channelid=channel.id)
        permittedmembers = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=ownerid)
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)

        if user.id == ownerid:
            if member.id in permittedmembers:
                await remove_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=member.id)
                await delete_current_permitted_user(bot=bot, channelid=channel.id, memberid=member.id)
                if member.id in modids:
                    await remove_mod(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=member.id)
                    embed = discord.Embed(title="Success", description=f"You removed from {member.mention} the mod status and blocked {member.mention}.")
                else:
                    embed = discord.Embed(title="Success", description=f"You kicked and blocked {member.mention}.")
            elif member.id in currentpermittedmembers:
                await delete_current_permitted_user(bot=bot, channelid=channel.id, memberid=member.id)
                embed = discord.Embed(title="Success", description=f"You kicked and blocked {member.mention}.")
            if status == 0 or status == 1: #unlocked or locked
                    await channel.set_permissions(target=member, connect=False)
            elif status == 2:
                await channel.set_permissions(target=member, connect=False, view_channel=False)

            await member.move_to(None, reason="Owner blocked this person")
        
        else:
            await add_blocked_person(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=member.id)
            embed = discord.Embed(title="Success", description=f"You blocked {member.mention}.")
        
        
        await interaction.response.send_message(embed=embed)

class UnBlockSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(UnBlockSelectMenu())

class UnBlockSelectMenu(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the member to unblock")

    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        guild = interaction.guild
        member = self.values[0]
        channel = interaction.channel
        user = interaction.user
        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        blocked_people = await get_blocked_member(bot=bot, guildid=guild.id, ownerid=ownerid)

        if member.id in blocked_people:
            if user.id == ownerid:
                await channel.set_permissions(target=member, connect=True)

            await remove_blocked_person(bot=bot, guildid=guild.id, ownerid=user.id, memberid=member.id)
            embed = discord.Embed(title="Success", description=f"You unblocked {member.mention}.")
        
        embed = discord.Embed(title="Success", description=f"You already unblocked {member.mention}.")
        
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
                await add_permitted_user(bot=bot, guildid=guild.id, ownerid=ownerid, memberid=self.values[0].id)
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
            embed = discord.Embed(title="Success", description=f"You removed <@{self.values[0]}> as a mod.")
        else:
            embed = discord.Embed(title="Error", description="You aren't the owner of this channel.")
        await interaction.response.send_message(embed=embed)

class KickSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(KickSelectMenu())

class KickSelectMenu(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the member to kick")

    async def callback(self, interaction: discord.Interaction):
        bot = interaction.client
        user = interaction.user
        channel = user.voice.channel
        guild = interaction.guild
        member = self.values[0]

        ownerid, name, status, vclimit, password = await get_current_cvc(bot=bot, channelid=channel.id)
        modids = await get_mods(bot=bot, guildid=guild.id, ownerid=ownerid)
        if user.id == ownerid or ownerid in modids:
            if member.id == ownerid:
                embed = discord.Embed(title="Error", description=f"You cant kick {member.mention}, because he is the owner of the channel.")
            elif member.id in modids:
                if user.id == ownerid:
                    embed = discord.Embed(title="Success", description=f"{user.mention} kicked {member.mention}.")
                    await member.move_to(None, reason="Owner or mods kicked this person.")
                else:
                    embed = discord.Embed(title="Error", description=f"You cant kick the mod {member.mention} as a mod.")
            elif member.voice.channel.id == channel.id:
                await member.move_to(None, reason="Owner or mods kicked this person.")
                embed = discord.Embed(title="Success", description=f"{user.mention} kicked {member.mention}.")
            else:
                embed = discord.Embed(title="Error", description=f"You cant kick {member.mention}, because he isnt in your channel.")
        else:
            embed = discord.Embed(title="Error", description=f"You cant kick {member.mention}, because you dont own this channel and arent a mod.")
        
        await interaction.response.send_message(embed=embed)