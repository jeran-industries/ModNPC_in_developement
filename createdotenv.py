import os

filepath="test.env"
try:
    os.remove(filepath)
except FileNotFoundError:
    pass

with open(filepath, 'a', encoding='utf-8') as f:
    token=input("Please enter your Discordbottoken! Enter nothing if you only want to test this bot out\n")
    if len(token) == 0:
        token = None
        f.write(f"Dc_token={token}\n")
    elif len(token) != 72:
        print("Hmm it can be that you didn't enter a Token. Please report this if you are sure it is a Token.")
        tokenverification=input("Enter y for 'I entered a token' or something else for 'my mistake i didnt enter a token'\n")
        if tokenverification == 'y' or tokenverification == 'Y' or tokenverification == 'yes':
            f.write(f"Dc_token='{token}'\n")
        else:
            token = None
            f.write(f"Dc_token={token}\n")
    else:
        f.write(f"Dc_token='{token}'\n")

    betatoken=input("Please enter your Discordbottoken for debugging! Enter nothing if you dont want go on developing this bot\n")
    if len(betatoken) == 0:
        betatoken = None
        f.write(f"Dc_token_beta={betatoken}\n")
    elif len(betatoken) != 72:
        print("Hmm it can be that you didn't enter a Token. Please report this if you are sure it is a Token.")
        betatokenverification=input("Enter y for 'I entered a token' or something else for 'my mistake i didnt enter a token'\n")
        if betatokenverification == 'y' or betatokenverification == 'Y' or betatokenverification == 'yes':
            f.write(f"Dc_token='{betatoken}'\n")
        else:
            betatoken = None
            f.write(f"Dc_token={betatoken}\n")
    else:
        f.write(f"Dc_token_beta='{betatoken}'\n")

    if token is None and betatoken is None:
        print("Hmm, you cant run this bot without any discordbottoken ._. Run this programm again and enter next time a token")
        os.remove(filepath)

    else:
        dc_bot_list_token=input("This bot supports a connection with https://discordbotlist.com You need for that a token from the website. Enter nothing if you dont want to list this bot.\n")
        if len(dc_bot_list_token) == 0:
            dc_bot_list_token = None
            f.write(f"Dc_bot_list_Token={dc_bot_list_token}\n")
        else:
            f.write(f"Dc_bot_list_Token='{dc_bot_list_token}'\n")

        print("Thats it for Tokens 🎉🎉🎉 Please enter now the channelids for monitoring your bot! The bot have to be able to view and send in these channels. Its best to give the bot admin rights on the server the channels are.\n")

        memberlogchannelid=input("Enter the channelid where new members and guilds will be logged.\n")
        if len(memberlogchannelid) == 0:
            memberlogchannelid = None
            f.write(f"Member_log_channel_ID={memberlogchannelid}\n")
        else:
            f.write(f"Member_log_channel_ID={memberlogchannelid}\n")

        reportchannelid=input("Enter the channelid where things like in rankcards will be reported to.\n")
        if len(reportchannelid) == 0:
            reportchannelid = None
            f.write(f"Report_channel_ID={reportchannelid}\n")
        else:
            f.write(f"Report_channel_ID={reportchannelid}\n")
  
        print("Success🎉🎉🎉, you can go back to ./README.md")