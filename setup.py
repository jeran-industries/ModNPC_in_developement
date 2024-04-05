import discord
import sqlite3
import aiosqlite
import asyncio

#own modules:
from checks import check4dm


async def setupcommand(interaction):
    if await check4dm(interaction) == False:
        member = interaction.user
        if member.guild_permissions.administrator:
            embeddedsetup = discord.Embed(title=f'Setup:', description = f'Here you can setup ModNPC', color=discord.Color.green())
            await interaction.response.send_message(embed = embeddedsetup, ephemeral = True, view = SelectStart())
        else:
            misssuccessembed = discord.Embed(title=f'Error', description = f'You dont have the rights to setup the bot.', color=discord.Color.dark_red())
            await interaction.response.send_message(embed = misssuccessembed, ephemeral = True)

#startselectmenu:
class SelectStart(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectStartMenu())

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Sucessfully given you {self.values}")

class SelectStartMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Anonymous Messages', description='Here you can activate, deactivate, set the cooldown of anonymous messages and limit them to channel.'),
            discord.SelectOption(label='Autoroles', description='Here you can add and remove autoroles.'),
            discord.SelectOption(label='Botupdates', description='You have to set a channel where the botupdates will be sent Otherwise the bot wont work.'),
            discord.SelectOption(label='Custom VCs', description='You can activate and deactivate custom voicechats.'),
            discord.SelectOption(label='Levelsystem', description='You can (de)activate the levelsystem, set the levelpingchannel, add and remove xp.'),
            discord.SelectOption(label='Logging', description='You can (de)activate the logging and set the loggingchannel.'),
            discord.SelectOption(label='Welcomemessages', description='You can (de)activate, set the welcomemessages and the channel where the message will be sent.'),
        ]
        super().__init__(placeholder="Choose what you want to change", options=options)

    async def callback(self, interaction: discord.Interaction):
        result = self.values[0]
        #print(result)
        if result == "Anonymous Messages":
            await anonymousmessagessetup(interaction)
        elif result == "Autoroles":
            await autorolessetup(interaction)
        elif result == "Botupdates":
            await botupdatessetup(interaction)
        elif result == "Custom VCs":
            await customvcsetup(interaction)
        elif result == "Levelsystem":
            await levelsystemsetup(interaction)
        elif result == "Logging":
            await logsetup(interaction)
        elif result == "Welcomemessages":
            await welcomemessagessetup(interaction)
        #await interaction.response.send_message(content=f"You clicked on this option: {result}")

#Autoroles:
async def autorolessetup(interaction):
    
    #return()

    member = interaction.user
    
    #print(labellist)

    await interaction.response.send_message("This part isnt completly programmed yet", ephemeral = True, view = ViewAutoRoleSetup())

class ViewAutoRoleSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        #self.add_item(Autorolelist(labellist = labellist))

    @discord.ui.button(label="Add Autorole", custom_id="addautorolebutton")
    async def addautorole(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view = ViewAutoRoleAddSetup(), ephemeral = True)

    @discord.ui.button(label="Remove Autorole", custom_id="removeautorolebutton", disabled = True)
    async def emoveautorole(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view = ViewAutoRoleRemoveSetup())

    @discord.ui.button(label="Reset Autoroles", custom_id="resetautorolebutton")
    async def resetautoroles(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if interaction.user.id == guild.owner.id:
            connection = await aiosqlite.connect("./database/database.db")
            connection.execute("DELETE FROM autorole WHERE guildid = ?", (guild.id))
            logchannelid = logchannelid[0]
            await connection.close()
            await interaction.response.send_message(f"All autoroles are deleted.", ephemeral = True)
        else:
            await interaction.response.send_message(f"You arent the owner of the server and cant reset it.", ephemeral = True)

    @discord.ui.button(label="List Autoroles", custom_id="listautorolesbutton")
    async def listautoroles(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        connection = await aiosqlite.connect("./database/database.db") #connect to polldatabase
        levelroleidcursor = await connection.execute("SELECT roleid FROM autorole WHERE guildid = ? AND membergroup = ?", (interaction.guild.id, 0))
        levelroleids = await levelroleidcursor.fetchall()
        await levelroleidcursor.close()
        membergroupcursor = await connection.execute("SELECT roleid FROM autorole WHERE guildid = ? AND membergroup = ?", (interaction.guild.id, 0))
        membergroups = await membergroupcursor.fetchall()
        await membergroupcursor.close()
        #print(levelroleid)
        await connection.close()
        try:
            levelroleids[0]
            for levelroleid, membergroup in levelroleids, membergroups:
                role = guild.get_role(levelroleid) 
                if membergroup == 0:
                    embed.add_field(name=role.name, value = f"Usergroup: All user")
                if membergroup == 1:
                    embed.add_field(name=role.name, value = f"Usergroup: Botuser")
                if membergroup == 2:
                    embed.add_field(name=role.name, value = f"Usergroup: Human user")
        except:
            embed = discord.Embed(title=f'You dont have any autorole yet.', color=discord.Color.light_grey())
        
        await interaction.response.send_message(embed = embed, ephemeral=True)
            

class ViewAutoRoleAddSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RoleSelectAutoRoleAddSetup())

class RoleSelectAutoRoleAddSetup(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the new role for your autorole.")

    async def callback(self, interaction: discord.Interaction):
        role = self.values[0]
        if role.is_assignable():
            await interaction.response.send_message(f"Who should be affected?", ephemeral = True, view = ViewAutoRoleUserGroupSetup(role=role))      
        else:
            message = await interaction.response.send_message(f"The role can't be assigned by the bot because the role is above the highest role of the bot.", ephemeral = True)

class ViewAutoRoleUserGroupSetup(discord.ui.View):
    def __init__(self, role):
        super().__init__(timeout=None)
        self.add_item(SelectAutoRoleUserGroupSetup(role=role))

class SelectAutoRoleUserGroupSetup(discord.ui.Select):
    def __init__(self, role):
        self.role = role
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
        guild = interaction.guild
        #all(0) usergroups: bot(1) and humanusers(2)
        connection = await aiosqlite.connect("./database/database.db")
        roleidsalluserscursor = await connection.execute('SELECT * FROM autorole WHERE guildid = ? AND roleid = ? AND membergroup = ?', (guild.id, role.id, 0))
        roleidsallusers = await roleidsalluserscursor.fetchone()
        await roleidsalluserscursor.close()

        roleidsbotuserscursor = await connection.execute('SELECT * FROM autorole WHERE guildid = ? AND roleid = ? AND membergroup = ?', (guild.id, role.id, 1))
        roleidsallbotusers = await roleidsbotuserscursor.fetchone()
        await roleidsbotuserscursor.close()

        roleidsallhumanuserscursor = await connection.execute('SELECT * FROM autorole WHERE guildid = ? AND roleid = ? AND membergroup = ?', (guild.id, role.id, 2))
        roleidsallhumanusers = await roleidsallhumanuserscursor.fetchone()
        await roleidsallhumanuserscursor.close()

        if roleidsallusers is not None and option == "Bots": #if there is already a autorole and selected option is bots
            await connection.execute("UPDATE autorole set membergroup = ? WHERE roleid = ?", (1, role.id))
            #await interaction.followup(f"You updated {self.role.name} and updated the assignement of the autorole from all users to only bots", ephemeral = True)
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and updated the assignement of the autorole from all users to only bot users", color=discord.Color.green())
        
        elif roleidsallusers is not None and option == "Humans": #if there is already a autorole and selected option is humans
            await connection.execute("UPDATE autorole set membergroup = ? WHERE roleid = ?", (2, role.id))
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and updated the assignement of the autorole from all users to only human users", color=discord.Color.green())
                
        elif roleidsallbotusers is not None and option != "Bots": #if there is already a autorole and selected option is human or all users
            await connection.execute("UPDATE autorole set membergroup = ? WHERE roleid = ?", (0, role.id))
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and set the assignement autorole from only botusers to be added to all users", color=discord.Color.green())

        elif roleidsallhumanusers is not None and option != "Humans": #if there is already a autorole and selected option is human or all users
            await connection.execute("UPDATE autorole set membergroup = ? WHERE roleid = ?", (0, role.id))
            embed = discord.Embed(title=f'SUCCESS', description = f"You updated {self.role.name} and set the assignement autorole from only human users to be added to all users", color=discord.Color.green())
        
        else:
            if option == "All users" and roleidsallusers is None:
                await connection.execute(f"INSERT INTO autorole VALUES ({guild.id}, {role.id}, 0)") #write into the table the data")
                embed = discord.Embed(title=f'SUCCESS', description = f"You created the autorole with {self.role.name} for all users", color=discord.Color.green())
            elif option == "Bots" and roleidsallbotusers is None:
                await connection.execute(f"INSERT INTO autorole VALUES ({guild.id}, {role.id}, 1)") #write into the table the data")
                embed = discord.Embed(title=f'SUCCESS', description = f"You created the autorole with {self.role.name} for all bot users", color=discord.Color.green())
            elif option == "Humans" and roleidsallhumanusers is None:
                await connection.execute(f"INSERT INTO autorole VALUES ({guild.id}, {role.id}, 2)") #write into the table the data")
                embed = discord.Embed(title=f'SUCCESS', description = f"You created the autorole with {self.role.name} for all human users", color=discord.Color.green())
            else:
                embed = discord.Embed(title=f'ERROR', description = f'This autorole is already created', color=discord.Color.red())

        await interaction.response.send_message(embed = embed, ephemeral = True)
        await connection.commit()
        await connection.close()

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
        file_name = "./database/database.db"
        connection = sqlite3.connect(file_name) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("UPDATE guildsetup set botupdatestatus = ? WHERE guildid = ?", (True, interaction.guild.id))
        cursor.execute("UPDATE guildsetup set botupdatechannelid = ? WHERE guildid = ?", (channel.id, interaction.guild.id))
        connection.commit()
        connection.close()
        embed = discord.Embed(title=f'Success', description=f"The botupdatechannel was set to https://discord.com/channels/{guild.id}/{channel.id}.\nAll commands can be now used.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral = True)

#Custom VCs:
async def customvcsetup(interaction):
    member = interaction.user
    await interaction.response.send_message("This part isnt programmed yet", ephemeral = True)

#Levelsystem:

async def levelsystemsetup(interaction):
    embeddedsetuplevelsystem = discord.Embed(title=f'Levelsystem Setup:', description = f'Here you activate, deactivate, reset and set the levelping', color=discord.Color.green())
    await interaction.response.send_message(embed = embeddedsetuplevelsystem, ephemeral = True, view = Buttons4LevelsystemSetup())

class Buttons4LevelsystemSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Activate", custom_id="LevelsystemSetupActivate", style=discord.ButtonStyle.green)
    async def levelsystemsetupactivate(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        file_name = "./database/database.db"
        connection = sqlite3.connect(file_name) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("UPDATE guildsetup set levelingsystemstatus = ? WHERE guildid = ?", (True, guild.id))
        connection.commit()
        connection.close()
        embed = discord.Embed(title=f'Success', description=f"You activated the levelsystem commands.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral = True)
    
    @discord.ui.button(label="Deactivate", custom_id="LevelsystemSetupDeactivate", style=discord.ButtonStyle.red)
    async def levelsystemsetupdeactivate(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        file_name = "./database/database.db"
        connection = sqlite3.connect(file_name) #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("UPDATE guildsetup set levelingsystemstatus = ? WHERE guildid = ?", (False, guild.id))
        connection.commit()
        connection.close()
        embed = discord.Embed(title=f'Success', description=f"You deactivated the levelsystem commands.", color=discord.Color.red())
        await interaction.response.send_message(embed = embed, ephemeral=True)
    
    @discord.ui.button(label="Add a levelrole", custom_id="AddALevelroleSetup", style=discord.ButtonStyle.grey)
    async def addalevelrolesetup(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=f'Add a new levelrole by setting the right level, the roleid and if it should be removed as soon you reach a new level:', color=discord.Color.light_grey())
        await interaction.response.send_message(embed = embed, ephemeral=True, view=LevelroleSelect())

    @discord.ui.button(label="Remove a levelrole", custom_id="RemoveALevelroleSetup", style=discord.ButtonStyle.grey)
    async def removealevelrolesetup(self, interaction: discord.Interaction, button: discord.ui.Button):
        connection = sqlite3.connect("./database/database.db") #connect to polldatabase
        cursor = connection.cursor()
        levelroleid = cursor.execute("SELECT roleid FROM levelroles WHERE guildid = ?", (interaction.guild.id, )).fetchall()
        #print(levelroleid)
        connection.close()
        if levelroleid is None:
            embed = discord.Embed(title=f'You dont have any levelroles yet.', color=discord.Color.light_grey())
            await interaction.response.send_message(embed = embed, ephemeral=True)
        else:
            levelroleoptions = [item[0] for item in levelroleid]
            #print(levelroleoptions)
            guild = interaction.guild
            embed = discord.Embed(title=f'Remove a levelrole by selecting it in the dropdownmenu:', color=discord.Color.light_grey())
            #role = discord.utils.get(guild.roles, id=roleid)
            labellist = []
            for i in levelroleoptions:
                role = discord.utils.get(guild.roles, id=i)
                labellist.append(discord.SelectOption(label=role.name, value=role.id))
            await interaction.response.send_message(embed = embed, ephemeral=True, view=LevelRole2RemoveSelect(levelroleoptions = labellist))


    @discord.ui.button(label="Set Levelping Channel", custom_id="LevelpingChannelSetup", style=discord.ButtonStyle.grey)
    async def levelpingchannelsetup(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=f'Set your levelpingchannel in this dropdownmenu:', color=discord.Color.light_grey())
        await interaction.response.send_message(embed = embed, ephemeral=False, view = ViewLevelPingSetup())

    @discord.ui.button(label="Reset (This can't be undone)", custom_id="LevelsystemSetupReset", style=discord.ButtonStyle.red)
    async def levelsystemsetupdereset(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        if interaction.user.id == guild.owner.id:
            file_name = "./database/database.db"
            connection = sqlite3.connect(file_name) #connect to polldatabase
            cursor = connection.cursor()
            cursor.execute("UPDATE membertable set messagessent = ? WHERE guildid = ?", (0, guild.id))
            cursor.execute("UPDATE membertable set voicetime = ? WHERE guildid = ?", (0, guild.id))
            cursor.execute("UPDATE membertable set xp = ? WHERE guildid = ?", (0, guild.id))
            #Set xp of every member to zero
            connection.commit()
            connection.close()
            embed = discord.Embed(title=f'Success', description=f"You reseted all memberstats of your guild.", color=discord.Color.green())
            await interaction.response.send_message(embed = embed, ephemeral=False)
        else:
            embed = discord.Embed(title=f'Error', description=f"For doing this you need to be an owner.", color=discord.Color.dark_red())
            await interaction.response.send_message(embed = embed, ephemeral=False)

class LevelroleRoleSelectMenu(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(placeholder="Choose the role:")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(LevelroleLevelModal(role=self.values))

class LevelroleSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(LevelroleRoleSelectMenu())

class LevelroleLevelModal(discord.ui.Modal, title="At which level do you get the role?"):
    def __init__(self, role):
        self.role = role
        super().__init__()
    
    sth = discord.ui.TextInput(label=f"Enter the level", placeholder="Enter the level, at which a member achieves the role", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=KeepRoleSelect(role=self.role, level=self.sth))

class KeepRoleSelectMenu(discord.ui.Select):
    def __init__(self, role, level):
        options = [
            discord.SelectOption(label='The member can keep the role', emoji='🟩'),
            discord.SelectOption(label="The member can't keep the role", emoji='🟥'),
        ]
        self.role = role
        self.level = level
        super().__init__(placeholder="Choose if the member can keep the role", options=options)

    async def callback(self, interaction: discord.Interaction):
        role = self.role
        level = self.level
        if self.values[0] == 'The member can keep the role':
            await interaction.response.send_message(content=f"You want to create a levelrole with the role {role[0].name} at the level {level}. The member can keep the role after getting the next levelrole.", view=CreateLevelrole(role=self.role, level=self.level, keeprole = True))
        elif self.values[0] == "The member can't keep the role":
            await interaction.response.send_message(content=f"You want to create a levelrole with the role {role[0].name} at the level {level}. The member can't keep the role after getting the next levelrole.", view=CreateLevelrole(role=self.role, level=self.level, keeprole = False))

class KeepRoleSelect(discord.ui.View):
    def __init__(self, role, level):
        super().__init__()
        self.add_item(KeepRoleSelectMenu(role=role, level=level))

class CreateLevelrole(discord.ui.View):
    def __init__(self, role, level, keeprole):
        self.role = role
        self.level = level
        self.keeprole = keeprole
        super().__init__(timeout=None)

    @discord.ui.button(label="Create", custom_id="create")
    async def createselfrolebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        roleid = int(self.role[0].id)
        connection = sqlite3.connect("./database/database.db") #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS levelroles (guildid INTEGER, roleid INTEGER, level INTEGER, keeprole BOOL)")
        if cursor.execute("SELECT * FROM levelroles WHERE roleid = ?", (roleid, )).fetchone() is None: 
            cursor.execute(f"INSERT INTO levelroles VALUES ({interaction.guild.id}, {self.role[0].id}, {self.level}, {self.keeprole})") #write into the table the data
            connection.commit()
            connection.close()
            await interaction.response.send_message(f"Success the levelrole was created.", ephemeral=True)
        else:
            await interaction.response.send_message(f"This role is already used.", ephemeral=True)

    @discord.ui.button(label="Discard", custom_id="discard")
    async def discardselfrolebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"You discarded the changes", ephemeral=True)

class LevelRole2RemoveSelectMenu(discord.ui.Select):
    def __init__(self, levelroleoptions):
        super().__init__(placeholder="Select the levelrole to remove it", options=levelroleoptions)

    async def callback(self, interaction: discord.Interaction):
        connection = sqlite3.connect("./database/database.db") #connect to polldatabase
        cursor = connection.cursor()
        cursor.execute("DELETE FROM levelroles WHERE roleid = ?", (self.values[0],))
        connection.commit()
        connection.close()
        await interaction.response.send_message(content=f"Success the levelrole was deleted.", ephemeral=True)

class LevelRole2RemoveSelect(discord.ui.View):
    def __init__(self, levelroleoptions):
        super().__init__()
        self.add_item(LevelRole2RemoveSelectMenu(levelroleoptions = levelroleoptions))

class ViewLevelReset(discord.ui.View): #in developement
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MentionableSelectLevelReset())

class MentionableSelectLevelReset(discord.ui.MentionableSelect):
    def __init__(self, custom_id = "mentionableselectlevelreset"):
        super().__init__(placeholder="Choose which member stats should be reseted.", channel_types=[discord.ChannelType.text, discord.ChannelType.news])

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        guild = interaction.guild
        file_name = "./database/database.db"
        connection = sqlite3.connect(file_name) #connect to polldatabase
        cursor = connection.cursor()
        print(f"{guild.id} || {channel.id}")
        cursor.execute("UPDATE guildsetup set levelingpingmessagechannel = ? WHERE guildid = ?", (channel.id, guild.id))
        connection.commit()
        connection.close()
        embed = discord.Embed(title=f'Success', description=f"The levelingpingmessagechannel was set to https://discord.com/channels/{guild.id}/{channel.id}.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral=True)

class ViewLevelPingSetup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ChannelSelectLevelPingSetup())

class ChannelSelectLevelPingSetup(discord.ui.ChannelSelect):
    def __init__(self, custom_id = "channelselectlevelpingsetup"):
        super().__init__(placeholder="Choose the channel where the levelpings will be send.", channel_types=[discord.ChannelType.text, discord.ChannelType.news])

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        guild = interaction.guild
        #try:
        file_name = "./database/database.db"
        connection = sqlite3.connect(file_name) #connect to polldatabase
        cursor = connection.cursor()
        #print(f"{guild.id} || {channel.id}")
        cursor.execute("UPDATE guildsetup set levelingpingmessagechannel = ? WHERE guildid = ?", (channel.id, guild.id))
        connection.commit()
        connection.close()
        embed = discord.Embed(title=f'Success', description=f"The levelingpingmessagechannel was set to https://discord.com/channels/{guild.id}/{channel.id}.", color=discord.Color.green())
        await interaction.response.send_message(embed = embed, ephemeral=True)

#Logs:
async def logsetup(interaction: discord.Interaction):
    member = interaction.user
    await interaction.response.send_message("This part isnt completly programmed yet and the setupmenu for logging is in beta. This is why some buttons are deactivated.", ephemeral = True)

class LogSetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Activate", custom_id="LogActivate")
    async def test(self, interaction: discord.Interaction, button: discord.ui.button):
        connection = await aiosqlite.connect("./database/database.db")
        guildid = interaction.guild.id
        logchannelidcursor = await connection.execute('SELECT logchannelid FROM guildsetup WHERE guildid = ?', (guildid,))
        logchannelid = await logchannelidcursor.fetchone()
        logchannelid = logchannelid[0]
        await connection.close()
        await logchannelidcursor.close()
        if logchannelid is not None:
            await interaction.response.send_message(f"Logging is already activated by setting the logging channel.", ephemeral = True)
        else:
            await interaction.response.send_message(f"Use first the button: `Set the logchannel`", ephemeral = True)        

    @discord.ui.button(label="Deactivate", custom_id="Logdeactivate")
    async def test(self, interaction: discord.Interaction, button: discord.ui.button):
        connection = await aiosqlite.connect("./database/database.db")
        guildid = interaction.guild.id
        await connection.execute("UPDATE guildsetup set logchannelid = ? WHERE guildid = ?", (0, guildid))
        await connection.commit()
        await connection.close()
        await interaction.response.send_message(f"You deactivated the logging", ephemeral = True)

    @discord.ui.button(label="Set the logchannel", custom_id="LogChannelSet")
    async def test(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"Use this command to set the logging channel: `/log_set_channel`", ephemeral = True)  

class LogChannelSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(WelcomemessageChannelSelectMenu())

class LogChannelSelectMenu(discord.ui.ChannelSelect):
    def __init__(self, custom_id = "ChannelSelectLog"):
        super().__init__(placeholder="Choose the channel where the log messages will be sent.", channel_types=[discord.ChannelType.text, discord.ChannelType.news])

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        channel = await channel.fetch() #converts APPCOMMANDCHANNEL to GUILDCHANNEL
        member = interaction.user
        connection = await aiosqlite.connect("./database/database.db")
        guildid = interaction.guild.id
        await connection.execute("UPDATE guildsetup set logchannelid = ? WHERE guildid = ?", (channel.id, guildid))
        await connection.commit()
        await connection.close()
        embed = discord.Embed(title = f"This channel was set to the logging channel.", description = f"This action was made by {member.mention} ||{member.id}||.")
        await channel.send(embed = embed)
        embed = discord.Embed(title = f"*SUCCESS*", description = f"You set the channel to {channel.mention}.")
        await interaction.response.send_message(embed = embed, ephemeral = True)

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

    @discord.ui.button(label="CreateWelcomemessage", custom_id="createwelcomemessage")
    async def createwelcomemessagebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        channelid = int(self.channel[0].id)
        headerwelcomemessage = self.headerwelcomemessage.value
        contentwelcomemessage = self.contentwelcomemessage.value
        connection = sqlite3.connect("./database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS welcomemessagetable (guildid INTEGER, channelid INTEGER, header TEXT, content TEXT)")
        cursor.execute("INSERT INTO welcomemessagetable VALUES (?, ?, ?, ?)", (interaction.guild.id, channelid, headerwelcomemessage, contentwelcomemessage))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"Success the welcomemessage was created. \n| {channelid} |\n| {headerwelcomemessage} |\n| {contentwelcomemessage} |", ephemeral=True)

    @discord.ui.button(label="DiscardWelcomemessage", custom_id="discardwelcomemessage")
    async def discardwelcomemessagebutton(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.send_message(f"You discarded the changes", ephemeral=True)