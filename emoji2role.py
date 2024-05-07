import os
import json

def emoji2role(file_name, emoji):
    if os.path.exists(file_name): #during creating a new reaction role, this function is used so a entry, which already excists, wont be recreated
        with open(file_name, encoding='utf-8') as f: #opening the right file with utf-8 as encoding
            emojis = json.load(f)["emojis"] #loading the dictionary file
        for e in emojis: #search for the right emoji in emoji
            if emoji == e['emoji']: #if right emoji found
                return(e['role']) #return the role