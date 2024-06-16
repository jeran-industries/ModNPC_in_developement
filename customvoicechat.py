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

#own modules:
from sqlitehandler import check4jointocreatechannel, check4savedcvc, check4currentcvc, get_cvc, insert_cvc, insert_into_current_cvctable, get_permitted_member

async def cvc(bot, member, beforechannel, afterchannel):
    if beforechannel is not None:
        await check4emptycvc(bot=bot, member=member, channel=beforechannel)

    if afterchannel is not None:
        await jointocreate(bot=bot, member=member, channel=afterchannel)
        
async def check4emptycvc(bot, member, channel):
    if len(channel.members) == 0 and await check4currentcvc(bot=bot, guildid=member.guild.id, ownerid=member.id, channelid=channel.id) is True:
        await channel.delete(reason = "Deleting a custom voicechannel because it is empty.")

async def jointocreate(bot, member, channel):
    guild=member.guild
    if channel is not None and await check4jointocreatechannel(bot=bot, guildid=guild.id, channelid=channel.id) is True: #check if member joins a channel and if the joined channel is the jointocreate channel (j2c)
        j2cchannel=channel
        if await check4savedcvc(bot=bot, guildid=guild.id, ownerid=member.id) is True:
            name, status, vclimit, password = await get_cvc(bot=bot, guildid=guild.id, ownerid=member.id)
            permitted_members = await get_permitted_member(bot=bot, guildid=guild.id, ownerid=member.id)
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
    else:
        print("Im here ig")

#async def check4voidchannel

class customvoicechatcontrolmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Rename", custom_id="renamecustomvoicechat")
    async def test(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Hey u clicked me... shame on u")