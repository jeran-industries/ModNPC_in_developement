#minigame:
#idea:
#buy kois with coins and merge them with other kois after that u can get a profit of coins or present them in your global rankprofile everywhere the levelsystem of the bot is active:
#different playstyles:
    #be safe and only merge kois with the same levels(100% success rate): only normal and unusual kois can be achieved:
        #merging different raritylevel will mix it, that means if u mix normal with unusual u get a 50/50 chance of getting normal pr unusual. 
        #mixing normal and rare will be a 32/32/32/4 chance of getting normal, unusual, rare and unreal kois(takes time to merge them)
    #play unsafe and merge kois with different levels(different success rates different from the leveldifference of the kois): unusual, rare, unreal and impossible
        #the higher the level difference the higher the odds that u get a better rarity level and that kois wont merge and die (takes time to merge them)
#get daily spins to get free kois
#get spins to get free kois with level higher then 1 by watching ads/opening a website(8cent with 1000 clicks)
#get gold spins by finishing quests and spins

#syntax:
#4x4 button/(embedded field with inline = True) layout for merging kois:
# __   __   __   __     __
#|__| |__| |__| |__| | |__| <- field to buy a lvl1 koi
# __   __   __   __     __
#|__| |__| |__| |__| | |__| <- field to edit your kois in your profile/opens also quest menu
# __   __   __   __     __
#|__| |__| |__| |__| | |__| <- field to get the daily spins/looking ads to get spins
# __   __   __   __     __
#|__| |__| |__| |__| | |__| <- field to sell a koi
#
#00001 | 00002 | 00004 | 00008
#00016 | 00032 | 00064 | 00128
#00256 | 00512 | 01028 | 02048
#04096 | 08192 | 16384 | 32768
#
#commands:
#!koimerge/k.merge:
#Opens the playfield
#!koispins/k.spins:
#Opens window with these fields
# ___________   ________   __________
#|daily spins| |ad spins| |gold spins|
# -----------   --------   ----------
#!koiquest/k.quest:
#Opens questwindow and list all quests and the progress
#
#database:
#membertable with this list:
#|   guildid    |            0             |             guildid             |
#|   memberid   |         memberid         |             memberid            |
#| messagessent |   messagessent(global)   |           messagessent          |
#|  voicetime   |     voicetime(global)    |            voicetime            |
#|      xp      |        xp(global)        |                xp               |
#|    status    | bansystemstatus(global)  |       status on the server      |
#|    joined    | first time joined the db | first time joined the server/db |

#koigametable with this list
#|   memberid     |
#|    guildid     |
#|     coins      |
#|  koi1display   |
#|  koi2display   |
#|  koi3display   |
#|     appid      |
#|   appopened?   |
#| koifield00001  |
#| koifield00002  |
#| koifield00004  |
#| koifield00008  |
#| koifield00016  |
#| koifield00032  |
#| koifield00064  |
#| koifield00128  |
#| koifield00256  |
#| koifield00512  |
#| koifield01028  |
#| koifield02048  |
#| koifield04096  |
#| koifield08192  |
#| koifield16384  |
#| koifield32768  |
#|    merging1    |
#|  merging1time  |
#|    merging2    |
#|  merging2time  |
#|    merging3    |
#|  merging3time  |
#|    merging4    |
#|  merging4time  |
#|    merging5    |
#|  merging5time  |
#|    merging6    |
#|  merging6time  |
#|    merging7    |
#|  merging7time  |
#|    merging8    |
#|  merging8time  |
#|     quest1     |
#|     quest2     |
#|     quest3     |
#|      daily     |
#|    daysinrow   |

#checklist:
#programming the syntax 
#koifishgraphics: different styles and rarity level (very difficult bez of the mass of different kois u need)
#appversion