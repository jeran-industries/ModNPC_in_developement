import json
import os
import io
import sqlite3
import discord

#own modules:
from link2id import link2serverid, link2channelid, link2messageid, channellink2channelid, channellink2guildid

async def poll_creating(interaction, bot, message, votecount, channel, option0, option1, option2, option3, option4, option5, option6, option7, option8, option9):
    ##v1 of pollsystem:
    #if option1 == None and option2 == None:
    #    ctx.reply("There are not enough choices so a poll can't be created!")
    #    return()
    #message_id = link2messageid(link)
    #channel_id = link2channelid(link)
    #server_id = link2serverid(link)
    #channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    #channel4poll = await bot.fetch_channel(channel_id4poll)
    #message = await channel.fetch_message(message_id)

    ##if votecount == '1' or votecount == '2' or votecount == '3' or votecount == '4' or votecount == '5' or votecount == '6' or votecount == '7' or votecount == '8' or votecount == '9' or votecount == '10':
    #if votecount == '1' or votecount == '2' or votecount == '3' or votecount == '4' or votecount == '5' or votecount == '6' or votecount == '7' or votecount == '8' or votecount == '9':    
    #    message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react     
    #    embed = discord.Embed(title="🗳 Poll", description = message.content, color=0x00ff00)
    #    message_of_the_poll = await channel4poll.send(embed=embed) #send a message without content to get messageid  
    #    running_status = True    
    #    file_name = './Polls/V1/' + str(server_id) + '/' + str(message_of_the_poll.id) + '.json' #getting the filename  
    #    if os.path.exists(file_name): #checking if filename already exists
    #        await ctx.reply('Error, there is already a poll existing! Please take another message!')
    #    else:
    #        new_embed = discord.Embed.from_dict(embed.to_dict())
    #        with open(file_name, 'a', encoding='utf-8') as f:
    #            data = {
    #                "data": [
    #                        {
    #                        "votecount": int(votecount),
    #                        "messagecontent": message.content,
    #                        "channel4poll": channel4poll.id,
    #                        "message_id_of_the_poll": message_of_the_poll.id,
    #                        "running-status": running_status,
    #                        "optioncounter": 0
    #                        }  
    #                ],
    #                "options": [
    #                                
    #                ]
    #            }
    #            json.dump(data, f, indent = 1) #writing data into json-file
    #            f.close()
    #        option_counter = 0

            #if option0 != None:
            #    await saving_option_4_poll(file_name, option0, new_embed, option_counter)
            #    await message_of_the_poll.add_reaction('0\ufe0f\u20e3') #adding the reaction to message
            #   option_counter = option_counter + 1
    #        if option1 != None:
    #            await saving_option_4_poll_v1(file_name, option1, new_embed, option_counter)
    #            option_counter = option_counter + 1

    #        if option2 != None:
    #            await saving_option_4_poll_v1(file_name, option2, new_embed, option_counter)
    #            option_counter = option_counter + 1
    #        
    #        if option3 != None:
    #            await saving_option_4_poll_v1(file_name, option3, new_embed, option_counter)
    #            option_counter = option_counter + 1
                
    #        if option4 != None:
    #            await saving_option_4_poll_v1(file_name, option4, new_embed, option_counter)
    #            option_counter = option_counter + 1

    #        if option5 != None:
    #            await saving_option_4_poll_v1(file_name, option5, new_embed, option_counter)
    #            option_counter = option_counter + 1

    #        if option6 != None:
    #            await saving_option_4_poll_v1(file_name, option6, new_embed, option_counter)
    #            option_counter = option_counter + 1

    #        if option7 != None:
    #            await saving_option_4_poll_v1(file_name, option7, new_embed, option_counter)
    #            option_counter = option_counter + 1

    #        if option8 != None:
    #            await saving_option_4_poll_v1(file_name, option8, new_embed, option_counter)
    #            option_counter = option_counter + 1

    #        if option9 != None:
    #            await saving_option_4_poll_v1(file_name, option9, new_embed, option_counter)
    #            option_counter = option_counter + 1
            
    #        with open(file_name, 'r+', encoding='utf-8') as f:# error: got a problem with writing right in json file
    #            data = json.load(f)
    #            polldata = data["data"]
    #            polldata[0]["optioncounter"] = option_counter
    #            with open(file_name, 'w', encoding='utf-8') as f:
    #                json.dump(data, f, indent = 1)
    #                f.close()
    #        await adding_number_reactions_to_polls_v1(file_name, bot)
    #        await message_of_the_poll.edit(embed=new_embed)
    #        await message_of_the_poll.add_reaction('\u23f8\ufe0f') #adding the reaction to message

    #else:
    #    await ctx.reply("Error, Votecount isnt a full number between 1 and 10")

    #v2 of pollsystem:
    member = interaction.user
    if option0 == None and option1 == None:
        await interaction.response.send_message("There are not enough choices so a poll can't be created!", ephemeral = True)
    elif member.guild_permissions.administrator:
        guildid = interaction.guild.id
        if votecount == 1 or votecount == 2 or votecount == 3 or votecount == 4 or votecount == 5 or votecount == 6 or votecount == 7 or votecount == 8 or votecount == 9 or votecount == 10:    
            #channel = await bot.fetch_channel(channel_id) #getting the channel from the message
            #message = await channel.fetch_message(message_id)
            embed = discord.Embed(title="🗳 Poll", description = message, color=0x00ff00)
            message_of_the_poll = await channel.send(embed=embed) #send a message without content to get messageid  
            file_name = './database/database.db' #getting the filename  database\database.db
            #message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react     
            new_embed = discord.Embed.from_dict(embed.to_dict())
            connection = sqlite3.connect(file_name) #connect to polldatabase
            cursor = connection.cursor()
            cursor.execute("INSERT INTO polldata VALUES (?, ?, ?, ?, ?)", (message_of_the_poll.id, channel.id, guildid, int(votecount), True)) #write into the table the data
            optionlist = [option0, option1, option2, option3, option4, option5, option6, option7, option8, option9]
            for index, option in enumerate(optionlist): #goes through the list of all available options
                if option != None: #does the option has content?
                    cursor.execute("INSERT INTO polloptions VALUES (?, ?, ?)", (index, message_of_the_poll.id, option)) #writes an option into the table
                    new_embed.add_field(name = option + " " + str(index) + "\ufe0f\u20e3", value = 0, inline = False) #adds a new field to the embedded message for each option
                    emoji = str(index) + "\ufe0f\u20e3"
                    await message_of_the_poll.add_reaction(emoji) #adds the reaction that can be clicked
                else:
                    connection.commit() #if the rest of the options has no content it saves it and close the database
                    connection.close()
                    break
            await message_of_the_poll.edit(embed=new_embed) #sending all the fields
            await message_of_the_poll.add_reaction('\u23f8\ufe0f') #adding the reaction to message
        else:
            await interaction.response.send_message("The votecount isnt 1, 2, 3, 4, 5, 6, 7, 8, 9 or 10!", ephemeral = True)
    else:
        await interaction.response.send_message("You cant create a poll!", ephemeral = True)


async def new_pollreaction_4_log(payload, bot):
    #server_id = payload.guild_id
    #message_id = payload.message_id
    #member_id = payload.user_id #getting member
    #emoji = payload.emoji.name 
    ##v1 of pollsystem:
    #file_name = "./Polls/V1/" + str(server_id) + "/" + str(message_id) + "_pollreactions.json"
    #if os.path.exists(file_name) and member_id != bot.user.id:
    #    new_data =  {
    #                        "member_id": member_id,
    #                        "emoji": emoji
    #                    }  
        
    #    with open(file_name, 'r', encoding = 'utf-8') as f:
    #        data = json.load(f) #loading the data in python for processing
    #    data["reactions"].append(new_data) #adding the new data in the already existing data
    #    with open(file_name, 'w', encoding = 'utf-8') as f:
    #        json.dump(data, f, indent = 1)                    
    #        f.close()
        
    #elif member_id != bot.user.id: #json file isnt created yet so the bot creates a file.
    #    with open(file_name, 'a', encoding = 'utf-8') as f: #creating file
    #        data = { #new data for the json-file
    #            "reactions": [
    #                {
    #                    "member_id": member_id,
    #                    "emoji": emoji
    #                }
    #            ]
    #        }
    #        json.dump(data, f, indent=1) #writing data into json-file
    #        f.close()
    
    #v2 of pollsystem:
    member_id = payload.user_id
    message_id = payload.message_id
    channel_id = payload.channel_id
    guild_id = payload.guild_id
    emoji = payload.emoji.name 
    file_name = "./database/database.db"
    if os.path.exists(file_name) and member_id != bot.user.id :
        guild = bot.get_guild(guild_id) #getting guild
        member = guild.get_member(member_id)
        channel = await bot.fetch_channel(channel_id) #getting the channel from the message
        message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react 
        connection = sqlite3.connect(file_name)
        cursor = connection.cursor()
        if cursor.execute("SELECT * FROM polldata WHERE messageid = ?", (int(message_id),)).fetchone() is not None: 
            #print(cursor.execute("SELECT messageid, runningstatus FROM polldata WHERE messageid = ?", (message_id,)).fetchone())
            #print(cursor.execute("SELECT emoji FROM polloptions WHERE optioncounter = ? AND messageid = ?", (emoji[-3], int(message_id))).fetchone())
            #print(cursor.execute("SELECT votecount FROM polldata WHERE messageid = ?", (int(message_id),)).fetchone())
            #print(cursor.execute("SELECT * FROM pollreactions WHERE messageid = ? AND member_id = ?", (int(message_id), int(member_id))).fetchone())
        
            cursor.execute("SELECT runningstatus FROM polldata WHERE messageid = ?", (int(message_id),))
            runningstatus = next(cursor, [None])[0]
            cursor.execute("SELECT votecount FROM polldata WHERE messageid = ?", (int(message_id),))
            votecount = next(cursor, [None])[0]

            #print(votecount)
            #print(len(cursor.execute("SELECT * FROM pollreactions WHERE messageid = ? AND member_id = ?", (int(message_id), int(member_id))).fetchall()))
            if runningstatus == True: #check if poll is running
                #check if there was already this reaction saved 
                if (cursor.execute("SELECT * FROM pollreactions WHERE messageid = ? AND member_id = ? AND emoji = ?", (int(message_id), member_id, emoji)).fetchone() is not None):
                    return
                elif emoji == '\u23f8\ufe0f' and member.guild_permissions.administrator: #reaction to stop poll
                    cursor.execute("UPDATE polldata set runningstatus = ? WHERE messageid = ?", (False, message_id)) #lookup if edit command can be used like that
                    await message.remove_reaction(emoji, member)
                    await message.remove_reaction(emoji, bot.user)
                    await message.add_reaction('\u23f9\ufe0f') #emoji to continue poll
                #check if used reaction is allowed and if the person trys to react too often
                elif (cursor.execute("SELECT optioncounter FROM polloptions WHERE optioncounter = ? AND messageid = ?", (int(emoji[-3]), int(message_id))).fetchone() is not None) and (votecount > len(cursor.execute("SELECT * FROM pollreactions WHERE messageid = ? AND member_id = ?", (int(message_id), int(member_id))).fetchall())):
                    cursor.execute("INSERT INTO pollreactions VALUES (?, ?, ?)", (int(message_id), member_id, emoji)) #saving data
                    embed = message.embeds[0]
                    i = int(emoji[-3])
                    embed.set_field_at(i, name=embed.fields[i].name, value=int(embed.fields[i].value) + 1, inline = False)    
                    await message.edit(embed=embed)
                else:
                    await message.remove_reaction(emoji, member) #remove reaction from user
            elif emoji == '\u23f9\ufe0f' and member.guild_permissions.administrator:
                await message.remove_reaction(emoji, member)
                await message.remove_reaction(emoji, bot.user)
                i=0
                for reaction in message.reactions:
                    await message.clear_reaction(reaction.emoji)
                    if emoji != '\u23f9\ufe0f':
                        await message.add_reaction(reaction.emoji)
                        embed.set_field_at(name = i, value=0, inline = False)
                    i = i + 1         
                #await adding_number_reactions_to_polls_v1(file_name, bot)
                cursor.execute("UPDATE polldata set runningstatus = ? WHERE messageid = ?", (True, message_id)) #lookup if edit command can be used like that
                await message.add_reaction('\u23f8\ufe0f') #emoji to stop poll
            else:
                await message.remove_reaction(emoji, member) #remove reaction from user
        connection.commit()
        connection.close()

async def remove_pollreaction_4_log(payload, bot):
    member_id = payload.user_id #getting member
    emoji = payload.emoji.name
    #v1 of pollsystem:
    #file_name = "./Polls/V1/" + str(server_id) + "/" + str(message_id) + "_pollreactions.json"
    #if os.path.exists(file_name):
    #    emoji = payload.emoji.name 
    #
    #    with open(file_name, 'r', encoding='utf-8') as f:
    #        data = json.load(f)
    #    reactions = data["reactions"]
    #    i=0
    #    for reaction in reactions:
    #        if emoji == reactions[i]["emoji"]:
    #            del reactions[i]
    #            break
    #        i = i + 1        
    #    with open(file_name, 'w', encoding='utf-8') as f:
    #        json.dump(data, f, indent=1)
    #        f.close()

    #v2 of pollsystem:
    channel_id = payload.channel_id
    message_id = payload.message_id
    file_name = "./database/database.db"
    connection = sqlite3.connect(file_name)
    cursor = connection.cursor()
    if member_id != bot.user.id and os.path.exists(file_name):
        if cursor.execute("SELECT * FROM polldata WHERE messageid = ?", (message_id,)).fetchone() is not None: 
            if cursor.execute("SELECT * FROM pollreactions WHERE messageid = ? AND member_id = ? AND emoji = ?", (message_id, member_id, emoji)).fetchone() is not None:
                cursor.execute("DELETE FROM pollreactions WHERE messageid = ? AND member_id = ? AND emoji = ?", (message_id, member_id, emoji))
                cursor.execute("SELECT runningstatus FROM polldata WHERE messageid = ?", (int(message_id),))
                runningstatus = next(cursor, [None])[0]
                if runningstatus == True:
                    channel = await bot.fetch_channel(channel_id) #getting the channel from the message
                    message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react 
                    embed = message.embeds[0]
                    i = int(emoji[-3])
                    embed.set_field_at(i, name=embed.fields[i].name, value=int(embed.fields[i].value) - 1, inline = False)    
                    await message.edit(embed=embed)
    connection.commit()
    connection.close()

    
#isnt needed anymore:
async def editingpollafternewreaction(payload, bot):
    channel_id = payload.channel_id
    channel = await bot.fetch_channel(channel_id) #getting the channel from the message
    message_id = payload.message_id
    message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react 
    server_id = payload.guild_id
    server = bot.get_guild(payload.guild_id) #getting guild
    member_id = payload.user_id #getting member
    member = server.get_member(member_id)
    emoji = payload.emoji.name
    #v1 of pollsystem:
    file_name = './Polls/V1/' + str(server_id) + '/' + str(message_id) + '.json' #getting the filename
    if (os.path.exists(file_name)) and (member_id != bot.user.id): #
        #print(f"Emoji: {emoji}, Administrator: {member.guild_permissions.administrator}, Member ID: {member_id}, Bot ID: {bot.user.id}")
        #if emoji == '0\ufe0f\u20e3' or emoji == '1\ufe0f\u20e3' or emoji == '2\ufe0f\u20e3' or emoji == '3\ufe0f\u20e3' or emoji == '4\ufe0f\u20e3' or emoji == '5\ufe0f\u20e3' or emoji == '6\ufe0f\u20e3' or emoji == '7\ufe0f\u20e3' or emoji == '8\ufe0f\u20e3' or emoji == '9\ufe0f\u20e3' or emoji == '\u23f8\ufe0f' or emoji == '\u25b6\ufe0f':
        if (emoji == '1\ufe0f\u20e3' or emoji == '2\ufe0f\u20e3' or emoji == '3\ufe0f\u20e3' or emoji == '4\ufe0f\u20e3' or emoji == '5\ufe0f\u20e3' or emoji == '6\ufe0f\u20e3' or emoji == '7\ufe0f\u20e3' or emoji == '8\ufe0f\u20e3' or emoji == '9\ufe0f\u20e3' or emoji == '\u23f8\ufe0f' or emoji == '\u23f9\ufe0f'): 
                with open(file_name, 'r+', encoding='utf-8') as f: #opening the right file with utf-8 as encoding
                    data = json.load(f)
                    polldata = data["data"]
                    votecount = polldata[0]["votecount"]
                    channel4poll_id = polldata[0]["channel4poll"]
                    channel4poll = await bot.fetch_channel(channel4poll_id) #getting the channel from the message
                    message_id_of_the_poll = polldata[0]["message_id_of_the_poll"]
                    message_of_the_poll = await channel4poll.get_partial_message(int(message_id_of_the_poll)).fetch() #getting the message to add a reaction so the user can more easy react             
                    running_status = polldata[0]["running-status"]
                    i = 0
                    if member_id != bot.user.id:
                        if emoji == '\u23f8\ufe0f' and member.guild_permissions.administrator:      #poll is stopped
                            polldata[0]["running-status"] = False
                            with open(file_name, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent = 1)
                                f.close()
                            await message_of_the_poll.remove_reaction(emoji, member)
                            await message_of_the_poll.remove_reaction(emoji, bot.user)
                            await message_of_the_poll.add_reaction('\u23f9\ufe0f') #emoji to continue poll
                        elif emoji == '\u23f9\ufe0f' and member.guild_permissions.administrator:    #poll is reseted
                            polldata[0]["running-status"] = True
                            with open(file_name, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent = 1)
                                f.close()
                            for reaction in message.reactions:
                                await message.clear_reaction(reaction.emoji)
                            await adding_number_reactions_to_polls_v1(file_name, bot)
                            await message_of_the_poll.add_reaction('\u23f8\ufe0f') #emoji to stop poll
                        else:
                            if running_status == True:
                                embed = message_of_the_poll
                                for embed in embed.embeds:
                                    for field in embed.fields:
                                        if emoji[-3] == field.name[-5]:
                                            if emoji[-3] == 0:
                                                field_name = 1
                                                field_value = int(field_name.value) + 1
                                                break
                                            field_name = field.name
                                            field_value = int(field.value) + 1
                                            break
                                        i = i + 1
                                embed.set_field_at(i, name=field_name, value=field_value, inline = False)
                                await message_of_the_poll.edit(embed=embed)
                                if (looking_number_of_reactions_of_member_up(message_id, server_id, member_id) > int(votecount)):
                                    await message_of_the_poll.remove_reaction(emoji, member) #remove reaction from user                        
        else:
            with open(file_name, 'r+', encoding='utf-8') as f: #opening the right file with utf-8 as encoding
                polldata = json.load(f)['data']
                message_id_of_the_poll = polldata[0]["message_id_of_the_poll"]
                channel4poll_id = polldata[0]["channel4poll"]
                channel4poll = await bot.fetch_channel(channel4poll_id)
                message_of_the_poll = await channel4poll.get_partial_message(int(message_id_of_the_poll)).fetch() #getting the message to add a reaction so the user can more easy react             
                await message_of_the_poll.remove_reaction(emoji, member) #remove reaction from user
    
    #v2 of pollsystem:
    #migrated to one simple function


#isnt needed anymore
async def editingpollafterremovedreaction(payload, bot):
    message_id = payload.message_id
    server_id = payload.guild_id
    member_id = payload.user_id #getting member
    emoji = payload.emoji.name
    file_name = './Polls/V1/' + str(server_id) + '/' + str(message_id) + '.json' #getting the filename
    if os.path.exists(file_name) and (emoji == '1\ufe0f\u20e3' or emoji == '2\ufe0f\u20e3' or emoji == '3\ufe0f\u20e3' or emoji == '4\ufe0f\u20e3' or emoji == '5\ufe0f\u20e3' or emoji == '6\ufe0f\u20e3' or emoji == '7\ufe0f\u20e3' or emoji == '8\ufe0f\u20e3' or emoji == '9\ufe0f\u20e3'): #during creating a new reaction role, this function is used so a entry, which already excists, wont be recreated
        if member_id != bot.user.id:
            with open(file_name, 'r+', encoding='utf-8') as f: #opening the right file with utf-8 as encoding
                data = json.load(f)
                polldata = data["data"]
                channel4poll_id = polldata[0]["channel4poll"]
                channel4poll = await bot.fetch_channel(channel4poll_id) #getting the channel from the message
                message_id_of_the_poll = polldata[0]["message_id_of_the_poll"]
                message_of_the_poll = await channel4poll.get_partial_message(int(message_id_of_the_poll)).fetch() #getting the message to add a reaction so the user can more easy react
                running_status = polldata[0]["running-status"]
                if running_status == True:
                    i = 0
                    embed = message_of_the_poll
                    for embed in embed.embeds:
                        for field in embed.fields:
                            if emoji[-3] == field.name[-5]:
                                field_name = field.name
                                field_value = int(field.value) - 1
                                print(emoji[-3])
                                print(field.name[-5])
                                print(i)
                                break
                            i = i + 1
                    embed.set_field_at(i, name=field_name, value=field_value, inline = False)
                    await message_of_the_poll.edit(embed=embed)

    #v2 of pollsystem:
    #migrated to one simple function


async def saving_option_4_poll_v1(file_name, option, new_embed, field_number):
    new_embed.add_field(name = option + " " + str(field_number + 1) + "\ufe0f\u20e3", value = 0, inline = False)
    new_option =  {
                    "option": option,
                }    
    with open(file_name,'r+', encoding = 'utf-8') as f: #open the already existing file
        options = json.load(f) #loading the data in python for processing
        options["options"].append(new_option) #adding the new data in the already existing data
        f.seek(0)
        json.dump(options, f, indent=1) #saving all the data
        f.close()
    return(new_embed)

def looking_number_of_reactions_of_member_up(message_id, server_id, member_id):
    file_name_reaction_log = './Polls/V1/' + str(server_id) + '/' + str(message_id) + '_pollreactions.json'
    number_of_reactions_of_member = 0
    i = 0
    with open(file_name_reaction_log, 'r', encoding='utf-8') as f:
        reactions = json.load(f)["reactions"]
        for reaction in reactions:
            if (reaction["member_id"] == member_id):
                number_of_reactions_of_member = number_of_reactions_of_member + 1
        return(number_of_reactions_of_member)
    
async def adding_number_reactions_to_polls_v1(file_name, bot):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            polldata = json.load(f)["data"]
            option_counter = polldata[0]["optioncounter"] 
            message_id = polldata[0]["message_id_of_the_poll"]            
            channel_id = polldata[0]["channel4poll"]
            channel = await bot.fetch_channel(channel_id) #getting the channel from the message
            message = await channel.get_partial_message(int(message_id)).fetch() #getting the message to add a reaction so the user can more easy react 
            emoji_counter = 1
            while option_counter >= emoji_counter:
                emoji = str(emoji_counter) + "\ufe0f\u20e3"
                await message.add_reaction(emoji)
                emoji_counter = emoji_counter + 1