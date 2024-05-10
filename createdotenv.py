import os

filepath=".env"
try:
    os.remove(filepath)
except FileNotFoundError:
    pass

with open(filepath, 'a', encoding='utf-8') as f:
    token=input("Please enter your Discordbottoken! Enter nothing if you only want to test this bot out\n")
    if len(token) == 0:
        token = None
        f.write(f"Dc_token={token}\n")
    else:
        f.write(f"Dc_token='{token}'\n")

    betatoken=input("Please enter your Discordbottoken for debugging! Enter nothing if you dont want go on developing this bot\n")
    if len(betatoken) == 0:
        betatoken = None
        f.write(f"Dc_token_beta={betatoken}\n")
    else:
        f.write(f"Dc_token_beta='{betatoken}'\n")

    dc_bot_list_token=input("This bot supports a connection with https://discordbotlist.com You need for that a token from the website. Enter nothing if you dont want to list this bot.\n")
    if len(dc_bot_list_token) == 0:
        dc_bot_list_token = None
        f.write(f"Dc_bot_list_Token={dc_bot_list_token}\n")
    else:
        f.write(f"Dc_bot_list_Token='{dc_bot_list_token}'\n")

    if token is None and betatoken is None:
        print("Hmm, you cant run this bot without any discordbottoken ._. Run this programm again and enter next time a token")
        os.remove(filepath) 
    else:    
        print("Success🎉🎉🎉, you can now run on windows python bot.py or on linux python3 bot.py")