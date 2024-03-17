def link2serverid(url):
    parts = url.split('/')
    server_id = parts[-3]
    #print(f"Server ID: {server_id}")  # prints '123456789012345678'
    return(int(server_id))

def link2channelid(url):
    parts = url.split('/')
    channel_id = parts[-2]
    #print(f"Channel ID: {channel_id}")  # prints '910111213141516171'
    return(int(channel_id))

def link2messageid(url):
    parts = url.split('/')
    message_id = parts[-1]
    return(int(message_id))

def channellink2channelid(url):
    parts = url.split('/')
    channel_id = parts[-1]
    return(int(channel_id))

def channellink2guildid(url):
    parts = url.split('/')
    channel_id = parts[-2]
    return(int(channel_id))