import discord
import sqlite3
import asyncio
import gettext

#own modules:
from checks import check4dm
from sqlitehandler import get_autorole, get_autoroles, update_autorole_2_other_membergroup, insert_autorole, delete_all_autoroles, update_logchannelid, activate_levelsystem, deactivate_levelsystem, update_voicetime, update_messagecounter, change_xp_by, get_levelrole, check4levelroles, create_levelrole, delete_levelrole, get_all_levelroleids, reset_memberstats, update_levelingpingchannel, insert_into_welcomemessage, activate_ticketsystem, deactivate_ticketsystem, update_channel_ticketsystem, get_ticketsystem_status, update_opentickets_category_ticketsystem, update_closedtickets_category_ticketsystem, delete_welcomemessage, update_logwebhookid, check4cvcstatus, change_customvc_status, de_activate_permission, get_permissions
from ticketsystem import OpenTicketButton

async def setupcommand(interaction, bot):
    if await check4dm(interaction) == False:
        member = interaction.user
        if member.guild_permissions.administrator:
            #text = gettext.translation(, localedir='locale', languages=['de_DE'])
            embeddedsetup = discord.Embed(title=f'Setup:', description = 'Here you can setup ModNPC.', color=discord.Color.green())
            await interaction.response.send_message(embed = embeddedsetup, ephemeral = True, view = SelectStart(bot))
        else:
            misssuccessembed = discord.Embed(title=f'Error', description = f'You dont have the rights to setup the bot.', color=discord.Color.dark_red())
            await interaction.response.send_message(embed = misssuccessembed, ephemeral = True)

#startselectmenu:
class SelectStart(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.add_item(SelectStartMenu(bot = bot))

class SelectStartMenu(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label='Anonymous Messages', description='Here you can activate, deactivate, set the cooldown of anonymous messages and limit them to channel.'),
            #discord.SelectOption(label='Applications', description='Here you can setup the applications for your server staff and other roles.'),
            discord.SelectOption(label='Autoroles', description='Here you can add and remove autoroles.'),
            discord.SelectOption(label='Botupdates', description='You have to set a channel where the botupdates will be sent Otherwise the bot wont work.'),
            discord.SelectOption(label='Custom VCs', description='You can activate and deactivate custom voicechats.'),
            discord.SelectOption(label='Levelsystem', description='You can (de)activate the levelsystem, set the levelpingchannel, add and remove xp.'),
            discord.SelectOption(label='Logging', description='You can (de)activate the logging and set the loggingchannel.'),
            discord.SelectOption(label='Ticketsystem', description='You can de(activate) the ticketsystem and select a channel for the ticketsystem.'),
            discord.SelectOption(label='Welcomemessages', description='You can (de)activate, set the welcomemessages and the channel where the message will be sent.'),
        ]
        super().__init__(placeholder="Choose what you want to change", options=options)

    async def callback(self, interaction: discord.Interaction):
        result = self.values[0]
        bot = self.bot
        #print(result)
        if result == "Anonymous Messages":
            await anonymousmessagessetup(interaction)
        elif result == "Applications":
            await applicationssetup(interaction)
        elif result == "Autoroles":
            await autorolessetup(interaction, bot)
        elif result == "Botupdates":
            await botupdatessetup(interaction)
        elif result == "Custom VCs":
            await customvcsetup(interaction)
        elif result == "Levelsystem":
            await levelsystemsetup(interaction, bot)
        elif result == "Logging":
            await logsetup(interaction, bot)
        elif result == "Ticketsystem":
            await ticketsystemsetup(interaction)
        elif result == "Welcomemessages":
            await welcomemessagessetup(interaction)
        #await interaction.response.send_message(content=f"You clicked on this option: {result}")

#Applications:
async def applicationssetup(interaction):
    pass

class ApplicationSetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    #@discord.ui.button(label="Add application")
    #async addnewapplication(self, interaction: discord.Interaction, button: discord.ui.Button):
    #    pass

#Autoroles:
async def autorolessetup(interaction, bot):
    
    #return()

    member = interaction.user
    
    #print(labellist)

    await interaction.response.send_message("This part isnt completly programmed yet", ephemeral = True, view = ViewAutoRoleSetup(bot))

class ViewAutoRoleSetup(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        #self.add_item(Autorolelist(labellist = labellist))

    @discord.ui.button(label="Add Autorole", custom_id="addautorolebutton")
    async def addautorole(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view = ViewAutoRoleAddSetup(bot=self.bot), ephemeral = True)

    @discord.ui.button(label="Remove Autorole", custom_id="removeautorolebutton", disabled = True)
    async def emoveautorole(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view = ViewAutoRoleRemoveSetup())

    @discord.ui.button(label="Reset Autoroles", custom_id="resetautorolebutton")
    async def resetautoroles(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if interaction.user.id == guild.owner.id:
            await delete_all_autoroles(bot=self.bot, guildid=guild.id)
            embed = discord.Embed(title='SUCCESS', description="All autoroles are deleted.", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral = True)
        else:
            embed = discord.Embed(title='ERROR', description="You arent the owner of the server and cant reset it.", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral = True)

    @discord.ui.button(label="List Autoroles", custom_id="listautorolesbutton")
    async def listautoroles(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        membergroups = [0, 1, 2]
        allmemberembed = discord.Embed(title='All users', color=discord.Color.dark_grey())
        allbotembed = discord.Embed(title='All bot users', color=discord.Color.dark_grey())
        allhumanembed = discord.Embed(title='All human users', color=discord.Color.dark_grey())

        for membergroup in membergroups:
                roleids = await get_autoroles(bot=self.bot, guildid=guild.id, membergroup=membergroup)
                for roleid in roleids:
                    if membergroup == 0:
                            role=guild.get_role(roleid)
                            allmemberembed.add_field(name="Role", value=role.mention, inline=False)
                    elif membergroup == 1:
                            role=guild.get_role(roleid)
                            allbotembed.add_field(name="Role", value=role.mention, inline=False)
                    elif membergroup == 2:
                            role=guild.get_role(roleid)
                            allhumanembed.add_field(name="Role", value=role.mention, inline=False)

        await interaction.response.send_message(embeds=[allmemberembed, allbotembed, allhumanembed], ephemeral=True)
            

class ViewAutoRoleAddSetup(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(RoleSelectAutoRoleAddSetup(bot=self.bot))

class RoleSelectAutoRoleAddSetup(discord.ui.RoleSelect):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(placeholder="Choose the new role for your autorole.")

    async def callback(self, interaction: discord.Interaction):
        role = self.values[0]
        if role.is_assignable():
            await interaction.response.send_message(f"Who should be affected?", ephemeral = True, view = ViewAutoRoleUserGroupSetup(role=role, bot=self.bot))      
        else:
            message = await interaction.response.send_message(f"The role can't be assigned by the bot because the role is above the highest role of the bot.", ephemeral = True)

class ViewAutoRoleUserGroupSetup(discord.ui.View):
    def __init__(self, role, bot):
        super().__init__(timeout=None)
        self.add_item(SelectAutoRoleUserGroupSetup(role=role, bot=bot))

class SelectAutoRoleUserGroupSetup(discord.ui.Select):
    def __init__(self, role, bot):
        self.role = role
        self.bot = bot
        options = [
            discord.SelectOption(label='All users', description='All user: Bots and humans', emoji='👤'),
            discord.SelectOption(label='Bots', description='Only Bots', emoji='🤖'),
            discord.SelectOption(label='Humans', description='Only Humans', emoji='🧑'),
        ]
        super().__init__(placeholder="Choose the group the role will be assigned to on joinup.", options=options)

    async def callback(self, interaction: discord.Interaction):
        #await interaction.response.defer()
        option=self.values[0]
        role = self.role
        bot = self.bot
        guild = interaction.guild
        #all(0) usergroups: bot(1) and humanusers(2)
        membergroups=[0, 1, 2]
        roleidsallusers=None
        roleidsallbotusers=None
        roleidsallhumanusers=None

        for membergroup in membergroups:
            if membergroup == 0:
                roleidsallusers = await get_autorole(bot=bot, membergroup=membergroup, roleid=role.id)
            if membergroup == 1:
                roleidsallbotusers = await get_autorole(bot=bot, membergroup=membergroup, roleid=role.id)
            if membergroup == 2:
                roleidsallbotusers = await get_autorole(bot=bot, membergroup=membergroup, roleid=role.id)

        if roleidsallusers is not None and option == "Bots": #if there is already a autorole and selected option is bots
            await update_autorole_2_other_membergroup(bot=bot, membergroup=1, roleid=role.id)
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and updated the assignement of the autorole from all users to only bot users", color=discord.Color.green())
        
        elif roleidsallusers is not None and option == "Humans": #if there is already a autorole and selected option is humans
            await update_autorole_2_other_membergroup(bot=bot, membergroup=2, roleid=role.id)
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and updated the assignement of the autorole from all users to only human users", color=discord.Color.green())
                
        elif roleidsallbotusers is not None and option != "Bots": #if there is already a autorole and selected option is human or all users
            await update_autorole_2_other_membergroup(bot=bot, membergroup=0, roleid=role.id)
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and set the assignement autorole from only botusers to be added to all users", color=discord.Color.green())

        elif roleidsallhumanusers is not None and option != "Humans": #if there is already a autorole and selected option is human or all users
            await update_autorole_2_other_membergroup(bot=bot, membergroup=0, roleid=role.id)
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and set the assignement autorole from only human users to be added to all users", color=discord.Color.green())
        
        else:
            if option == "All users" and roleidsallusers is None:
                await insert_autorole(bot=bot, guildid=guild.id, roleid=role.id, membergroup=0)
                embed = discord.Embed(title=f'SUCCESS', description = f"You created the autorole with {self.role.name} for all users", color=discord.Color.green())
            elif option == "Bots" and roleidsallbotusers is None:
                await insert_autorole(bot=bot, guildid=guild.id, roleid=role.id, membergroup=1)
                embed = discord.Embed(title=f'SUCCESS', description = f"You created the autorole with {self.role.name} for all bot users", color=discord.Color.green())
            elif option == "Humans" and roleidsallhumanusers is None:
                await insert_autorole(bot=bot, guildid=guild.id, roleid=role.id, membergroup=2)
                embed = discord.Embed(title=f'SUCCESS', description = f"You created the autorole with {self.role.name} for all human users", color=discord.Color.green())
            else:
                embed = discord.Embed(title=f'ERROR', description = f'This autorole is already created', color=discord.Color.red())

        await interaction.response.send_message(embed = embed, ephemeral = True)

class ViewAutoRoleRemoveSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RoleSelectAutoRoleRemoveSetup())

class RoleSelectAutoRoleRemoveSetup(discord.ui.RoleSelect):
    def __init__(self, custom_id = "roleselectautoroleremovesetup"):
        super().__init__(placeholder="Choose the autorole you want to remove.")

    async def callback(self, interaction: discord.Interaction):
        pass

#Anonymous Messages:

async def anonymousmessagessetup(interaction):
    member = interaction.user
    await interaction.response.send_message("This part isnt programmed yet", ephemeral = True)
    #if member.guild_permissions.administrator:
        #filename = "./database/database"
        #connection = sqlite3.connect(filename)
        #cursor = connection.cursor()
        #cursor.execute("UPDATE guildsetup set anonymousmessagestatus = ? WHERE guildid = ?", (True, interaction.guild.id))
        #cursor.execute("UPDATE guildsetup set anonymousmessagecooldown = ? WHERE guildid = ?", (cooldown, interaction.guild.id))
        #connection.commit()
        #connection.close()
    #else:
        #misssuccessembed = discord.Embed(title=f'Error', description = f'You dont have the rights to do that', color=discord.Color.dark_red())
        #await interaction.response.send_message(embed = misssuccessembed, ephemeral = True)
    
class SelectAnonymousMessage(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectAnonymousMessage())

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Sucessfully given you {self.values}")

#Botupdates:

async def botupdatessetup(interaction):
    embeddedsetupbotupdates = discord.Embed(title=f'Botupdates Setup:', description = f'Here you can set the botupdatechannel of ModNPC', color=discord.Color.green())
    await interaction.response.send_message(embed = embeddedsetupbotupdates, ephemeral = True, view = ViewBotupdateSetup())
    #file_name = "./database/database.db"
    #connection = sqlite3.connect(file_name) #connect to polldatabase
    #cursor = connection.cursor()
    #cursor.execute("UPDATE guildsetup set botupdatechannelid = ?", (channel.id,))
    #embed = discord.Embed(title=f'Success', description=f"The botupdatechannel was set to {channel}. All commands can be now used.", color=discord.Color.green())
    #await interaction.response.send_message(embed = embed)

class ViewBotupdateSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ChannelSelectBotupdateSetup())

class ChannelSelectBotupdateSetup(discord.ui.ChannelSelect):
    def __init__(self, custom_id = "channelselectbotupdatesetup"):
        super().__init__(placeholder="Choose the channel where the botupdates will be send.", channel_types=[discord.ChannelType.text])

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        channel = await channel.fetch() #converts APPCOMMANDCHANNEL to GUILDCHANNEL
        bot = interaction.client
        guild = interaction.guild
        newschannelid = 1191732882092339270
        newschannel = await bot.fetch_channel(newschannelid)
        await newschannel.follow(destination = channel)
        #file_name = "./database/database.db"
        #connection = sqlite3.connect(file_name) #connect to polldatabase
        #cursor = connection.cursor()
        #cursor.execute("UPDATE guildsetup set botupdatestatus = ? WHERE guildid = ?", (True, interaction.guild.id))
        #cursor.execute("UPDATE guildsetup set botupdatechannelid = ? WHERE guildid = ?", (channel.id, interaction.guild.id))
        #connection.commit()
        #connection.close()
        embed = discord.Embed(title=f'Success', description=f"The botupdatechannel was set to https://discord.com/channels/{guild.id}/{channel.id}.\nAll commands can be now used.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral = True)

#Custom VCs:
async def customvcsetup(interaction):
    bot = interaction.client
    guild=interaction.guild
    embed = discord.Embed(title="Custom Voicechats")
    cvcstatus=await check4cvcstatus(bot=bot, guildid=guild.id)
    if cvcstatus is False:
        await interaction.response.send_message(embed=embed, view=activButtonCVcSetup(), ephemeral = True)
    else:
        member = interaction.user
        await interaction.response.send_message("This part isnt programmed yet, just delete the channel for now :).", ephemeral = True)
        await change_customvc_status(bot=bot, status=False, guildid=guild.id)

class activButtonCVcSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Activate", custom_id="CVcSetupActivate", style=discord.ButtonStyle.green)
    async def levelsystemsetupactivate(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot = interaction.client
        guild = interaction.guild
        customvcscategory = await guild.create_category(name = "| Custom VCs |")
        join2createchannel = await customvcscategory.create_voice_channel(name="Join to create")
        await change_customvc_status(bot=bot, status=True, guildid=guild.id, channelid=join2createchannel.id)
        embed = discord.Embed(title=f'Success', description=f"You activated Custom VCs. Test it here out: {join2createchannel.mention}.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral = True)

#Levelsystem:

async def levelsystemsetup(interaction, bot):
    embeddedsetuplevelsystem = discord.Embed(title=f'Levelsystem Setup:', description = f'Here you activate, deactivate, reset and set the levelping', color=discord.Color.green())
    await interaction.response.send_message(embed = embeddedsetuplevelsystem, ephemeral = True, view = Buttons4LevelsystemSetup(bot))

class Buttons4LevelsystemSetup(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Activate", custom_id="LevelsystemSetupActivate", style=discord.ButtonStyle.green)
    async def levelsystemsetupactivate(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        await activate_levelsystem(bot=self.bot, guildid=guild.id)
        embed = discord.Embed(title=f'Success', description=f"You activated the levelsystem commands.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral = True)
    
    @discord.ui.button(label="Deactivate", custom_id="LevelsystemSetupDeactivate", style=discord.ButtonStyle.red)
    async def levelsystemsetupdeactivate(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        await deactivate_levelsystem(bot=self.bot, guildid=guild.id)
        embed = discord.Embed(title=f'Success', description=f"You deactivated the levelsystem commands.", color=discord.Color.red())
        await interaction.response.send_message(embed = embed, ephemeral=True)
        
    @discord.ui.button(label="Reset (This can't be undone)", custom_id="LevelsystemSetupReset", style=discord.ButtonStyle.red)
    async def levelsystemsetupdereset(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        bot = self.bot
        if interaction.user.id == guild.owner.id:
            await reset_memberstats(bot=bot, guildid=guild.id)
            #Set xp of every member to zero
            embed = discord.Embed(title=f'Success', description=f"You reseted all memberstats of your guild.", color=discord.Color.green())
            await interaction.response.send_message(embed = embed, ephemeral=False)
        else:
            embed = discord.Embed(title=f'Error', description=f"For doing this you need to be an owner.", color=discord.Color.dark_red())
            await interaction.response.send_message(embed = embed, ephemeral=False)

    @discord.ui.button(label="Set Levelping Channel", custom_id="LevelpingChannelSetup", style=discord.ButtonStyle.grey)
    async def levelpingchannelsetup(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=f'Set your levelpingchannel in this dropdownmenu:', color=discord.Color.light_grey())
        await interaction.response.send_message(embed = embed, ephemeral=True, view = ViewLevelPingSetup(bot=self.bot))
    
    @discord.ui.button(label="Add a levelrole", custom_id="AddALevelroleSetup", style=discord.ButtonStyle.grey, row=2)
    async def addalevelrolesetup(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=f'Add a new levelrole by setting the right level, the roleid and if it should be removed as soon you reach a new level:', color=discord.Color.light_grey())
        await interaction.response.send_message(embed = embed, ephemeral=True, view=LevelroleSelect(bot=self.bot))

    @discord.ui.button(label="Remove a levelrole", custom_id="RemoveALevelroleSetup", style=discord.ButtonStyle.grey, row=2)
    async def removealevelrolesetup(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot = self.bot
        guild = interaction.guild
        checklevelrole = await check4levelroles(bot=bot, guildid=guild.id)
        if checklevelrole == False:
            embed = discord.Embed(title=f'You dont have any levelroles yet.', color=discord.Color.light_grey())
            await interaction.response.send_message(embed = embed, ephemeral=True)
        else:
            #levelroleoptions = [item[0] for item in levelroleid]
            #print(levelroleoptions)
            levelroleids=await get_all_levelroleids(bot=bot, guildid=guild.id)
            print(levelroleids)
            embed = discord.Embed(title=f'Remove a levelrole by selecting it in the dropdownmenu:', color=discord.Color.light_grey())
            #role = discord.utils.get(guild.roles, id=roleid)
            labellist = []
            for levelroleid in levelroleids:
                levelrole = discord.utils.get(guild.roles, id=levelroleid)
                labellist.append(discord.SelectOption(label=levelrole.name, value=levelrole.id),)
            print(labellist)
            await interaction.response.send_message(embed = embed, ephemeral=True, view=LevelRole2RemoveSelect(bot=bot, levelroleoptions = labellist))

class LevelroleSelect(discord.ui.View):
    def __init__(self, bot):
        self.bot=bot
        super().__init__()
        self.add_item(LevelroleRoleSelectMenu(bot))

class LevelroleRoleSelectMenu(discord.ui.RoleSelect):
    def __init__(self, bot):
        self.bot=bot
        super().__init__(placeholder="Choose the role:")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(LevelroleLevelModal(bot=self.bot, role=self.values))

class LevelroleLevelModal(discord.ui.Modal, title="At which level do you get the role?"):
    def __init__(self, bot, role):
        self.role = role
        self.bot = bot
        super().__init__()
    
    sth = discord.ui.TextInput(label=f"Enter the level", placeholder="Enter the level, at which a member achieves the role", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=KeepRoleSelect(bot=self.bot, role=self.role, level=self.sth), ephemeral=True)

class KeepRoleSelectMenu(discord.ui.Select):
    def __init__(self, bot, role, level):
        options = [
            discord.SelectOption(label='The member can keep the role', emoji='🟩'),
            discord.SelectOption(label="The member can't keep the role", emoji='🟥'),
        ]
        self.role = role
        self.level = level
        self.bot = bot
        super().__init__(placeholder="Choose if the member can keep the role", options=options)

    async def callback(self, interaction: discord.Interaction):
        role = self.role
        level = self.level
        bot = self.bot
        if self.values[0] == 'The member can keep the role':
            await interaction.response.send_message(content=f"You want to create a levelrole with the role {role[0].name} at the level {level}. The member can keep the role after getting the next levelrole.", view=CreateLevelrole(bot=self.bot, role=self.role, level=self.level, keeprole = True), ephemeral=True)
        elif self.values[0] == "The member can't keep the role":
            await interaction.response.send_message(content=f"You want to create a levelrole with the role {role[0].name} at the level {level}. The member can't keep the role after getting the next levelrole.", view=CreateLevelrole(bot=self.bot, role=self.role, level=self.level, keeprole = False), ephemeral=True)

class KeepRoleSelect(discord.ui.View):
    def __init__(self, bot, role, level):
        super().__init__()
        self.add_item(KeepRoleSelectMenu(bot=bot, role=role, level=level))

class CreateLevelrole(discord.ui.View):
    def __init__(self, bot, role, level, keeprole):
        self.role = role
        self.level = level
        self.keeprole = keeprole
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Create", custom_id="create")
    async def createselfrolebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        roleid = int(self.role[0].id)
        bot=self.bot
        if await get_levelrole(bot=bot, roleid=roleid) == False: 
            guildid=interaction.guild.id
            level=self.level
            keeprole=self.keeprole
            await create_levelrole(bot=bot, guildid=guildid, roleid=roleid, level=level, keeprole=keeprole)
            await interaction.response.send_message(f"Success the levelrole was created.", ephemeral=True)
        else:
            await interaction.response.send_message(f"This role is already used.", ephemeral=True)

    @discord.ui.button(label="Discard", custom_id="discard")
    async def discardselfrolebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"You discarded the changes", ephemeral=True)

class LevelRole2RemoveSelect(discord.ui.View):
    def __init__(self, bot, levelroleoptions):
        self.bot = bot
        super().__init__()
        self.add_item(LevelRole2RemoveSelectMenu(bot=self.bot, levelroleoptions = levelroleoptions))

class LevelRole2RemoveSelectMenu(discord.ui.Select):
    def __init__(self, bot, levelroleoptions):
        self.bot = bot
        super().__init__(placeholder="Select the levelrole to remove it", options=levelroleoptions)

    async def callback(self, interaction: discord.Interaction):
        await delete_levelrole(bot=self.bot, roleid=self.values[0])
        await interaction.response.send_message(content=f"Success the levelrole was deleted.", ephemeral=True)

class ViewLevelPingSetup(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(ChannelSelectLevelPingSetup(bot))

class ChannelSelectLevelPingSetup(discord.ui.ChannelSelect):
    def __init__(self, bot, custom_id = "channelselectlevelpingsetup"):
        super().__init__(placeholder="Choose the channel where the levelpings will be send.", channel_types=[discord.ChannelType.text, discord.ChannelType.news])

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        guild = interaction.guild
        bot = interaction.client
        await update_levelingpingchannel(bot=bot, channelid=channel.id, guildid=guild.id)
        embed = discord.Embed(title=f'Success', description=f"The levelpingmessagechannel was set to https://discord.com/channels/{guild.id}/{channel.id}.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral=True)

#Logs:
async def logsetup(interaction: discord.Interaction, bot):
    member = interaction.user
    embed = discord.Embed(title = f"*LOGGING SETUP*")
    await interaction.response.send_message(embed=embed, view=LogSetupView(bot=bot), ephemeral = True)

class LogSetupView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Set the logchannel", custom_id="LogChannelSet")
    async def logchannelselect(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(view=LogChannelSelect(bot = self.bot), ephemeral = True)
        #await interaction.response.send_message(f"Use this command to set the logging channel: `/log_set_channel`", ephemeral = True)  

    @discord.ui.button(label="Deactivate", custom_id="LogDeactivate")
    async def deactivate(self, interaction: discord.Interaction, button: discord.ui.button):
        await update_logchannelid(bot=self.bot, logchannelid=0, guildid=interaction.guild.id)
        embed = discord.Embed(title = f"*SUCCESS*", description = f"You deactivated the logging")
        await interaction.response.send_message(embed=embed, ephemeral = True)

class LogChannelSelect(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(LogChannelSelectMenu(bot=self.bot))

class LogChannelSelectMenu(discord.ui.ChannelSelect):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(placeholder="Choose the channel where the log messages will be sent.", channel_types=[discord.ChannelType.text, discord.ChannelType.news])

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        bot = self.bot
        member = interaction.user
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            channel = await channel.fetch()
            webhook = await channel.create_webhook(name="ModNPC Logging", reason="Created Webhook for Logging")
            testembed = discord.Embed(title = f"This is a testmessage.", description = f"This action was made by {member.mention} ||{member.id}||.")
            try:
                testmessage = await channel.send(embed=testembed)
                try:
                    await testmessage.create_thread(name="testhread")
                    guildid = interaction.guild.id
                    await update_logchannelid(bot=bot, logchannelid=channel.id, guildid=guildid)
                    await update_logwebhookid(bot=bot, logwebhookid=webhook.id, guildid=guildid)
                    embed = discord.Embed(title = f"This channel was set to be the logging channel.", description = f"This action was made by {member.mention} ||{member.id}||.")
                    await channel.send(embed = embed)
                    embed = discord.Embed(title = f"*SUCCESS*", description = f"You set the channel to {channel.mention}.\nI always recommand activating the permission: `administrator`") 
                except :
                    embed = discord.Embed(title = f"Hmm something went wrong", description = f"Please check this permissions: \n`create public threads`")
                await testmessage.delete()
            except:
                embed = discord.Embed(title = f"Hmm something went wrong", description = f"Please activate these permissions: \n`send messages`\n`send messages in threads`\n`create public threads`")
        except:
            embed = discord.Embed(title = f"Hmm something went wrong", description = f"Please activate these permissions: \n`view channel`\n`manage webhooks`\n`send messages`\n`send messages in threads`\n`create public threads`")
        await interaction.followup.send(embed = embed, ephemeral = True)

async def ticketsystemsetup(interaction: discord.Interaction):
    bot = interaction.client
    guild = interaction.guild
    ticketsystem_status = await get_ticketsystem_status(bot=bot, guildid=guild.id)
    if ticketsystem_status is None or ticketsystem_status=="None":
        ticketsystem_status = False
    else:
        ticketsystem_status = False
    print(ticketsystem_status)
    if ticketsystem_status is False:
        embed= discord.Embed(title="Ticketsystem Setup", description=f"Here you can activate. and select the channel for the channel to create a ticket. Please note that by selecting a channel, the selected channel will be cleaned up.")
        await interaction.response.send_message(embed=embed, view=activateticketsystemsetupview(), ephemeral = True)
    if ticketsystem_status is True:
        embed= discord.Embed(title="Ticketsystem Setup", description=f"Here you can deactivate and select the channel for the channel to create a ticket. Please note that by selecting a channel, the selected channel will be cleaned up.")
        await interaction.response.send_message(embed=embed, view=deactivateticketsystemsetupview(), ephemeral = True)
    
class activateticketsystemsetupview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Activate", custom_id="activateticketsystem")
    async def ActivateScript(self, interaction: discord.Interaction, button: discord.ui.button):
        await activate_ticketsystem(bot=interaction.client, guildid=interaction.guild.id)
        passembed=discord.Embed(title=f"Ticketsystem activated!!!")
        await interaction.response.send_message(embed=passembed, ephemeral = True)

    @discord.ui.button(label="Select Channel", custom_id="ticketsystemchannelselect")
    async def SelectChannelActivateScript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title=f"Here you can select the channel where to open a ticket.")
        await interaction.response.send_message(embed=embed, view = TicketsystemChannelView(), ephemeral = True)

    @discord.ui.button(label="Add processor", custom_id="ticketsystemaddsupporter")
    async def AddSupporterScript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title=f"Here you can add people and roles for processing tickets.")
        await interaction.response.send_message(embed=embed, view = TicketsystemAddProcessorSelect(), ephemeral = True)

    @discord.ui.button(label="Remove processor", custom_id="ticketsystemremovesupporter")
    async def RemoveSupporterScript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title=f"Here you can remove people and roles for processing tickets.")
        await interaction.response.send_message(embed=embed, view = TicketsystemRemoveProcessorSelect(), ephemeral = True)

class deactivateticketsystemsetupview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Deactivate", custom_id="deactivateticketsystem")
    async def DeactivateScript(self, interaction: discord.Interaction, button: discord.ui.button):
        await deactivate_ticketsystem(bot=interaction.client, guildid=interaction.guild.id)
        passembed=discord.Embed(title=f"Ticketsystem deactivated!!!")
        await interaction.response.send_message(embed=passembed, ephemeral = True)

    @discord.ui.button(label="Select Channel", custom_id="ticketsystemchannelselect")
    async def SelectChannelDeactivateScript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title=f"Here you can select the channel where to open a ticket.")
        await interaction.response.send_message(embed=embed, view = TicketsystemChannelView(), ephemeral = True)

    @discord.ui.button(label="Add processor", custom_id="ticketsystemaddsupporter")
    async def AddSupporterScript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title=f"Here you can add people and roles for processing tickets.")
        await interaction.response.send_message(embed=embed, view = TicketsystemAddProcessorSelect(), ephemeral = True)

    @discord.ui.button(label="Remove processor", custom_id="ticketsystemremovesupporter")
    async def RemoveSupporterScript(self, interaction: discord.Interaction, button: discord.ui.button):
        embed=discord.Embed(title=f"Here you can remove people and roles for processing tickets.")
        await interaction.response.send_message(embed=embed, view = TicketsystemRemoveProcessorSelect(), ephemeral = True)

class TicketsystemChannelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketsystemChannelSelectChannel())

class TicketsystemChannelSelectChannel(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(placeholder="Enter the channel where you can start a ticket", channel_types=[discord.ChannelType.text, discord.ChannelType.news])

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        bot = interaction.client
        guild = interaction.guild
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            channel = await channel.fetch() #converts APPCOMMANDCHANNEL to GUILDCHANNEL
            try:
                testembed = discord.Embed(title="Testembed")
                testmessage = await channel.send(embed = testembed)
                await testmessage.delete()
            except:
                runningtestembed = discord.Embed(title="ERROR", description=f"The bot can't send messages in this channel. Please make sure to activate `send messages` for the bot in {channel.mention}")    
                await interaction.followup.send(embed=runningtestembed)
                channel = None
            finally:
                if channel is not None:
                    runningtestembed = discord.Embed(title=f"SUCCESS - Tests completed \nSending ticketmessage in {channel.mention} and creating categories.")    
                    await interaction.followup.send(embed=runningtestembed)

                    await update_channel_ticketsystem(bot=bot, guildid=guild.id, channelid=channel.id)
                    ticketembed = discord.Embed(title="Create a ticket", description="Create a ticket and descripe your issue in the modal.")
                    await channel.send(embed = ticketembed, view=OpenTicketButton())
                    
                    #create categories:
                    openticketcategory = await guild.create_category(name = "Open Tickets")
                    closedticketcategory = await guild.create_category(name = "Closed Tickets")

                    await openticketcategory.set_permissions(target=guild.default_role, read_messages=False, send_messages=False)
                    await closedticketcategory.set_permissions(target=guild.default_role, read_messages=False, send_messages=False)

                    await update_opentickets_category_ticketsystem(bot=bot, guildid=guild.id, categoryid=openticketcategory.id)
                    await update_closedtickets_category_ticketsystem(bot=bot, guildid=guild.id, categoryid=closedticketcategory.id)
                    

        except TypeError or ValueError:
            runningtestembed = discord.Embed(title="ERROR", description=f"The bot can't view the channel. Please make sure to activate `view channel` and `send messages` for the bot in {channel.mention}")
            await interaction.followup.send(embed=runningtestembed)
        #await interaction.response.send_message(content=f"Sucessfully given you {channel}")

class TicketsystemAddProcessorSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketsystemAddProcessorMentionableSelect())

class TicketsystemAddProcessorMentionableSelect(discord.ui.MentionableSelect):
    def __init__(self):
        super().__init__(placeholder="Enter the role or user who will be allowed to process tickets.")

    async def callback(self, interaction: discord.Interaction):
        mentionables = self.values
        bot=interaction.client
        guild=interaction.guild
        if isinstance(mentionables[0], discord.Role) is True: #Mentionable is a role
            role = mentionables[0]
            await de_activate_permission(bot=bot, guildid=guild.id, status=True, permission="ticketprocessor", roleid=role.id)
            embed = discord.Embed(title="You added a role as a ticketprocessor", description=f"You added {role.mention} as a ticketprocessor")
        else: #Mentionable is a member
            member = mentionables[0]
            await de_activate_permission(bot=bot, guildid=guild.id, status=True, permission="ticketprocessor", memberid=member.id)
            embed = discord.Embed(title="You added a member as a ticketprocessor", description=f"You added {member.mention} as a ticketprocessor")
        await interaction.response.send_message(embed=embed)

class TicketsystemRemoveProcessorSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketsystemRemoveProcessorMentionableSelect())

class TicketsystemRemoveProcessorMentionableSelect(discord.ui.MentionableSelect):
    def __init__(self):
        super().__init__(placeholder="Enter the role or user who will be removed from process tickets.")

    async def callback(self, interaction: discord.Interaction):
        mentionables = self.values
        bot=interaction.client
        guild = interaction.guild

        roleids, memberids = await get_permissions(bot=bot, permission="ticketprocessor", guildid=guild.id)

        if isinstance(mentionables[0], discord.Role) is True: #Mentionable is a role
            if mentionables[0].id in roleids:
                role = mentionables[0]
                await de_activate_permission(bot=bot, guildid=guild.id, status=False, permission="ticketprocessor", roleid=role.id)
                embed = discord.Embed(title="You removed a role as a ticketprocessor.", description=f"You removed {role.mention} as a ticketprocessor.")
            else:
                embed = discord.Embed(title="This role never got access to the ticketsystem.")

        else: #Mentionable is a member
            if mentionables[0].id in memberids:
                member = mentionables[0]
                await de_activate_permission(bot=bot, guildid=guild.id, status=False, permission="ticketprocessor", memberid=member.id)
                embed = discord.Embed(title="You removed a member as a ticketprocessor.", description=f"You removed {member.mention} as a ticketprocessor.")
            else:
                embed = discord.Embed(title="This member never got access to the ticketsystem.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

#Welcomemessages:
async def welcomemessagessetup(interaction: discord.Interaction):
    embed= discord.Embed(title=f"Here you can set a welcomemessage up.")
    await interaction.response.send_message(embed=embed, view=WelcomemessageChannelSelect(), ephemeral = True)

class WelcomemessageChannelSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(WelcomemessageChannelSelectMenu())

class WelcomemessageChannelSelectMenu(discord.ui.ChannelSelect):
    def __init__(self, custom_id = "ChannelSelectWelcomemessage"):
        super().__init__(placeholder="Choose the channel where the welcomemessage will be sent.", channel_types=[discord.ChannelType.text, discord.ChannelType.news])

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(WelcomemessageModal(channel=self.values))

class WelcomemessageModal(discord.ui.Modal, title="What is the welcomemessage?"):
    def __init__(self, channel):
        self.channel = channel
        super().__init__()
    
    headerwelcomemessage = discord.ui.TextInput(label=f"Enter the header of the welcomemessage", style=discord.TextStyle.paragraph)
    contentwelcomemessage = discord.ui.TextInput(label=f"Enter the header of the welcomemessage", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=WelcomemessageConfirmation(channel=self.channel, headerwelcomemessage = self.headerwelcomemessage, contentwelcomemessage = self.contentwelcomemessage), ephemeral=True)

class WelcomemessageConfirmation(discord.ui.View):
    def __init__(self, channel, headerwelcomemessage, contentwelcomemessage):
        self.channel = channel
        self.headerwelcomemessage = headerwelcomemessage
        self.contentwelcomemessage = contentwelcomemessage
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Welcomemessage", custom_id="createwelcomemessage")
    async def createwelcomemessagebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        channelid = int(self.channel[0].id)
        headerwelcomemessage = self.headerwelcomemessage.value
        contentwelcomemessage = self.contentwelcomemessage.value
        bot = interaction.client
        guild = interaction.guild
        await delete_welcomemessage(bot=bot, guildid=guild.id)
        await insert_into_welcomemessage(bot=interaction.client, guildid=interaction.guild.id, channelid=channelid, headerwelcomemessage=headerwelcomemessage, contentwelcomemessage=contentwelcomemessage)
        successembed = discord.Embed(title="SUCCESS", description=f"Success the welcomemessage was created for <#{channelid}>.")
        await interaction.response.send_message(embed=successembed, ephemeral=True)

    @discord.ui.button(label="Discard Welcomemessage", custom_id="discardwelcomemessage")
    async def discardwelcomemessagebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        successembed = discord.Embed(title="SUCCESS", description=f"You discarded the changes")
        await interaction.response.send_message(embed=successembed, ephemeral=True)