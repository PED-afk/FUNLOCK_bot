import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import subprocess
import time
import math
import random
from pathlib import Path
import platform

from data_manage import save_json, load_json


#users
ME=616710497378631709
BOT_ROLE=1516075439347470437

#channel(s)
BOTS_CHANNEL_ID = 1515333724269445270 #real chat

"""
MAIN=1514351967265095720
SECONDARY=1516056331365122170
BLUE=1514605988861448253
GREEN=1514606141320069260
YELLOW=1514606190510739556
"""


# Set up the bot with a command prefix
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

def chooseFaceFromCategory(category:str):
    if category in bot.faces:
        faces=bot.faces[category]
    else:
        faces=["(face category not found)"]
    r=random.randint(0,len(faces)-1)
    return faces[r]

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    #cleanup
    async for msg in bot.get_channel(BOTS_CHANNEL_ID).history(limit=None):
        try:
            await msg.delete()
        except discord.Forbidden:
            print("I don't have permission to delete this messages.")
            break
        except discord.HTTPException:
            pass
    
    face=chooseFaceFromCategory("big_eyes")

    with open(bot.hotboot_file,"r") as f:
        if int(f.readline().strip())==0:
            await bot.get_channel(BOTS_CHANNEL_ID).send(f"I'm awake!\nGood morning!\n {face}")
        else:
            await bot.get_channel(BOTS_CHANNEL_ID).send(f"Back online! {face}")

    if not tick.is_running():
        tick.start()


@bot.event
async def on_message(message):
    if message.author.bot or message.webhook_id is not None or message.author == bot.user:
        return
    idSTR=str(message.author.id)
    if str(message.author.id) not in bot.user_data.keys():
        bot.user_data[idSTR]={}
        bot.user_data[idSTR]["main"]="None"
        bot.user_data[idSTR]["steamID"]="None"
        bot.user_data[idSTR]["steamID3"]="None"
        bot.user_data[idSTR]["steamID64"]="None"
        bot.user_data[idSTR]["money"]=0
        bot.user_data[idSTR]["items"]=[]
        bot.user_data[idSTR]["lvl"]=0
        bot.user_data[idSTR]["XP"]=0
        bot.user_data[idSTR]["hidden"]={}
        bot.user_data[idSTR]["hidden"]["messageCD"]=0
    else:
        if message.content[0]!="!" and time.time()>=bot.user_data[idSTR]["hidden"]["messageCD"]:
            bot.user_data[idSTR]["hidden"]["messageCD"]=time.time()+bot.messageCD
            bonusM=1

            users_in_voice = []

            for guild in bot.guilds:
                for voice_channel in guild.voice_channels:
                    for member in voice_channel.members:
                        users_in_voice.append(f"{member} in {voice_channel.name} ({guild.name})")
            if len(users_in_voice)!=0:
                givesBonus={
                "good luck":{"bonus":0.5,"alias":{"name":" gl ","bonus":0.25}},
                "have fun":{"bonus":0.5,"alias":{"name":" hf ","bonus":0.25}},
                }
                for i,key in enumerate(givesBonus):
                    if key in message.content:
                        bonusM+=givesBonus[key]["bonus"]
                    elif givesBonus[key]["alias"]["name"] in message.content:
                        bonusM+=givesBonus[key]["alias"]["bonus"]

            lenght=len(message.content)//10
            bot.user_data[idSTR]["money"]+=100+random.randint(0,lenght)*bonusM
            bot.user_data[idSTR]["XP"]+=1+random.randint(0,lenght)*bonusM
            level=bot.user_data[idSTR]["lvl"]
            if bot.user_data[idSTR]["XP"]>=100+2**(level/4)+level:
                bot.user_data[idSTR]["XP"]-=100+2**(level/4)+level
                bot.user_data[idSTR]["lvl"]+=1
    
    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    senderID=ctx.author.id
    if ctx.channel.id == BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            #await ctx.send(f"TEST:\nDeleted command message?\n{chooseFaceFromCategory("question")}",delete_after=10)
            await ctx.send(f"TEST:\nNothing to test\n.=.",delete_after=10)
            #await ctx.send(f"TEST:\n```is this copyable?```",delete_after=10)
            print("command")

@bot.command()
async def start(ctx):
    senderID=ctx.author.id
    if ctx.channel.id == BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel to be able to start a timer.")
            else:
                if bot.timers[ctx.author.voice.channel.category.name[-2]]==None:
                    bot.timers[ctx.author.voice.channel.category.name[-2]]=bot.startTimers[ctx.author.voice.channel.category.name[-2]]
                    await ctx.reply("Started timer.")
                    
                    name=ctx.author.voice.channel.name[-2]
                    names=[]
                    for guild in bot.guilds:
                        for channel in discord.utils.get(guild.categories, name=f"[{name}]").voice_channels:
                            for member in channel.members:
                                if member.global_name=="PurpleEarthDragon":
                                    names.append(member.global_name+chooseFaceFromCategory("love"))
                                else:
                                    names.append(member.global_name)
                    
                    await ctx.send(f"__Good luck, and Have fun!__\n"+'\n'.join(names)+"\n"+chooseFaceFromCategory("happy"),delete_after=bot.startTimer)
                else:
                    await ctx.reply("There is already an active timer in this voice channel category.")
        else:
            await ctx.reply("You don't have permission! >:)",delete_after=10)
        
@bot.command()
async def shutdown(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        me=await bot.fetch_user(ME)
        if senderID==ME:
            if ctx.guild.voice_client:
                await ctx.guild.voice_client.disconnect()
            save_json(bot.user_data_path,bot.user_data)
            await ctx.reply("Shuting down.\nGood night!\nᴗ˳ᴗ",delete_after=10)
            with open(bot.restart_file,"w") as f:
                f.write("0")
            await bot.close()
        elif any(role.id == BOT_ROLE for role in ctx.author.roles):
            await ctx.send("Sorry only `"+str(me)+"` can shut me down.\n(Because then he knows I'm not running.)",delete_after=10)
            
@bot.command(aliases=["reload"])
async def restart(ctx,save:str="save"):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.guild.voice_client:
                await ctx.guild.voice_client.disconnect()
            if save=="save":
                save_json(bot.user_data_path,bot.user_data)
            with open(bot.restart_file,"w") as f:
                f.write("1")
            await ctx.reply("Shuting down.\nBe right back!\n"+chooseFaceFromCategory("blush_happy"),delete_after=20)
            await bot.close()

@bot.command() #aliases=["reload"] dont work on raspberry
async def sleep(ctx,save:str="save"):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.guild.voice_client:
                await ctx.guild.voice_client.disconnect()
            if save=="save":
                save_json(bot.user_data_path,bot.user_data)
            
            with open(bot.restart_file,"w") as f:
                f.write("2")
            with open(bot.pause_file,"r") as f:
                pauseStart=int(f.readline().strip())
                pauseEnd=int(f.readline().strip())
            
            await ctx.reply(f"Going to sleep\nI will be unavailable between {pauseStart} and {pauseEnd} CEST\n"+chooseFaceFromCategory("sleep"),delete_after=20)
            await bot.close()
        

@bot.command()
async def end(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel so I know which timer to end.")
            else:
                if bot.timers[ctx.author.voice.channel.category.name[-2]]>time.time()-1:
                    bot.timers[ctx.author.voice.channel.category.name[-2]]=time.time()-1
                    await ctx.reply("Timer stoped.")

@bot.command()
async def endit(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel so I know which timer to end.")
            else:
                if bot.timers[ctx.author.voice.channel.category.name[-2]]!=None:
                    bot.timers[ctx.author.voice.channel.category.name[-2]]=None
                    await ctx.reply("Timer stoped. Moving noone.")

@bot.command()
async def settimer(ctx,x:float):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel to change a timer lenght.")
            else:
                bot.startTimers[ctx.author.voice.channel.category.name[-2]]=x*60
                await ctx.reply(f"Starting time set to {x} minutes.")
            
@bot.command()
async def gettimer(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel to view a timer lenght.")
            else:
                await ctx.reply(f"The timer is set to {bot.startTimers[ctx.author.voice.channel.category.name[-2]]/60} minutes.")

@bot.command()
async def bot_help(ctx, section:str=None):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        anyView=True
        if section==None:
            anyView=True
            botcommands=[
                "`!bot_help timer`: Commands about my timer functionality.",
                "`!bot_help voice`: Commands about me using voice channels.",
                "`!bot_help admin`: Commands that only 'important' people can use.",
                "`!bot_help minigame`: Commands about a minigame that is in early development.",
                "`!bot_help extra`: Commands about a no particular topic.",
            ]
        elif section=="timer":
            anyView=True
            botcommands=[
                f"`!start` and `!start second`: Start an x minute timer. When the timer ends I put everyone into the `Deadlock [#]` channel (from lane channels).\n(Timer lenght is configureable; only 1 timer can be used at the same time (as right no there is only 1 set of lane channels))",
                "`!end`: Ends the timer and moves everyone immediately.",
                f"`!endit`: Ends the timer without sending people to the `Deadlock [#]` channel.",
                "`!settimer x`: Set the timer lenght to x minutes.",
                "`!gettimer`: Tells you the timer lenght.",
                "`!remaining:` Tells you how much time remains on the timer.",
            ]
        elif section=="voice":
            face=chooseFaceFromCategory("annoyed")
            anyView=True
            botcommands=[
                f"`!join`: I will join `Deadlock [#]` and will use an experimental feature to automate my timer functionality.",
                f"`!leave`: I will leave `Deadlock [#]` but will contionue counting for the timer.",
                f"(feature is not possible {face}, but I can be there for emotional support."
            ]
        elif section=="admin":
            anyView=False
            botcommands=[
                "`!Ping`: I will send 'Pong!' if I'm alive.",
                "`!status`: My version, OS and hardware I run on.",
                "`!sleep`: I will sleep until a certain hour to save on energy and hardware integrity. (the bot is unavailable during sleep but will automatically start at* the designated hour)"
                "`!restart:` or `!reload`: I will restart and apply changes to my code.",
                "`!clear_loaded`: I forget stuff so I don't save incorrect data.",
                "`!shutdown`: Kill me :("
            ]
        elif section=="minigame":
            anyView=True
            botcommands=[
                "Some data collection for now, maybe roles or nicknames later?\n(Also steamid for lane assign logic if there ever be a way for it.)",
                "`!set_main`: Set this to your most played character so others can know.",
                "`!set_steam_id`: Add your steam id to the \"database\"",
                "`!my_data`: I will tell you what data I have on you.",
                "`!remove_me`: I will remove your data from the \"database\"",
                "`!save`: Save from variable to a file. (will save automaticaly on shutdown and restart)",
            ]
        elif section=="extra":
            anyView=True
            botcommands=[
                "`!source`: Lobotomy (source code)"
            ]
        else:
            await ctx.reply("No command 'folder' exist with that name.")
            return

        if (senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles)) or anyView:
            if len(botcommands)!=0:
                await ctx.reply('\n'.join(botcommands))


@bot.command()
async def Ping(ctx):
    if ctx.channel.id==BOTS_CHANNEL_ID:
        await ctx.reply("Pong!",delete_after=2)

@bot.command()
async def Pat(ctx):
    if ctx.channel.id==BOTS_CHANNEL_ID:
        await ctx.reply(chooseFaceFromCategory("pat"))

@bot.command()
async def remaining(ctx):
    if ctx.channel.id==BOTS_CHANNEL_ID:
        senderID=ctx.author.id
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel to view a timer.")
            else:
                if bot.startTimers[ctx.author.voice.channel.category.name[-2]]!=None:
                    await ctx.reply(f"Remaining time: {round(abs(bot.startTimers[ctx.author.voice.channel.category.name[-2]]-time.time())/60,3)} min(s).")
                else:
                    await ctx.reply("Timer is not active.")

@bot.command()
async def status(ctx):
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if ctx.author.name=="PurpleEarthDragon":
            face=chooseFaceFromCategory("annoyed")
            l="."
            for i in face:
                l+=" "
            l+="(Why do you want to know?)"
            await ctx.reply(f"{l}\n{face}´")
        winlin=platform.system()
        cpu=platform.machine()
        try:
            lindistr=platform.freedesktop_os_release()
        except:
            lindistr=None
        curTime=time.time()//1
        diff=curTime-bot.bootTime
        hours=diff//60//60
        diff-=diff//60//60*60*60
        minutes=diff//60
        diff-=diff//60*60
        seconds=diff
        extra=""
        if hours>2:
            extra=f"\nI'm tired. "+chooseFaceFromCategory("tired")
        await ctx.reply(f"I'm fully operating.\nVersion: {bot.version}\nOS:\n{winlin}\nHardware I'm living on:\n{cpu}\nI've been running for: {hours} hours, {minutes} minutes and {seconds} seconds.{extra}")
        if lindistr!=None:
            await ctx.send("Fun fact: Most likely I'm running on a rasberry pi 5. :D\nLinux dist: "+lindistr["PRETTY_NAME"],delete_after=30)

@bot.command()
async def join(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.guild.voice_client!=None:
                await ctx.reply(f"Sorry I'm busy in another channel. "+chooseFaceFromCategory("nervous"))
            else:
                if ctx.author.voice==None:
                    await ctx.reply("You must be in a voice channel so I know which channel to join.")
                else:
                    channel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.category.name)
                    await channel.connect()

@bot.command()
async def leave(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.voice_client:
                if ctx.author.voice==None:
                    await ctx.reply("You must be in a voice channel so I know if you are allowed to make me leave.")
                else:
                    if ctx.author.voice.channel == ctx.voice_client.channel:
                        await ctx.guild.voice_client.disconnect()
            else:
                await ctx.reply("I'm not in any voice channels.")

@bot.command()
async def source(ctx):
    if ctx.channel.id==BOTS_CHANNEL_ID:
        file=discord.File(Path(__file__))
        await ctx.reply("My brain:",file=file)

@bot.command()
async def set_main(ctx,main:str):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        character=[
            "Abrams",
            "Apollo",
            "Bebop",
            "Billy",
            "Calico",
            "Celeste",
            "The Doorman",
            "Drifter",
            "Dynamo",
            "Graves",
            "Grey Talon",
            "Haze",
            "Holliday",
            "Infernus",
            "Ivy",
            "Kelvin",
            "Lady Geist",
            "Lash",
            "McGinnis",
            "Mina",
            "Mirage",
            "Mo & Krill",
            "Paige",
            "Paradox",
            "Pocket",
            "Rem",
            "Seven",
            "Shiv",
            "Silver",
            "Sinclair",
            "Venator",
            "Victor",
            "Vindicta",
            "Viscous",
            "Vyper",
            "Warden",
            "Wraith",
            "Yamato"
        ]
        if main in character:
            bot.user_data[str(senderID)]["main"]=main
        else:
            await ctx.reply("That is not a valid character.")

@bot.command()
async def set_steam_id(ctx,id:int):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        bot.user_data[str(senderID)]["steamID"]=str(id)

@bot.command()
async def my_data(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        message=""
        for i, (key,data) in enumerate(bot.user_data[str(senderID)].items()):
            if key=="hidden":
                break
            if key=="items" and len(data)==0:
                break
            if key=="steamID3" or key=="steamID64":
                break
            message+=f"{key}: {data}\n"
        await ctx.reply(message)
        
@bot.command()
async def remove_me(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        bot.user_data[str(senderID)]={
            "main":"None",
            "steamID":"None",
            "steamID3":"None",
            "steamID64":"None",
            "money":0,
            "items":[],
            "lvl":0,
            "XP":0
        }

@bot.command()
async def save(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            save_json(bot.user_data_path,bot.user_data)
            await ctx.reply("Saving some stuff. "+chooseFaceFromCategory("concentrate"),delete_after=10)

@bot.command()
async def clear_loaded(ctx, section:str=None):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME:
            bot.user_data={}





@tasks.loop(seconds=1)
async def tick():
    for i, (name,time) in enumerate(bot.timers.items()):
        if time!=None:
            timer=timer//1
            curTime=time.time()//1
            if timer-curTime==60:
                await bot.get_channel(BOTS_CHANNEL_ID).send(f"1 minute remaining on the [{name}] timer.",delete_after=60)
            elif timer<=curTime:
                await bot.get_channel(BOTS_CHANNEL_ID).send(f"Moving people in category [{name}].",delete_after=60)
                for guild in bot.guilds:
                    category = discord.utils.get(guild.categories, name=f"[{name}]")
                    TARGET=discord.utils.get(category.voice_channels, name=f"Deadlock [{name}]").id
                    SOURCES=[]
                    for other in category.voice_channels:
                        if other.id!=TARGET:
                            SOURCES.append(other.id)
                for channel in SOURCES:
                    people=[]
                    lane=bot.get_channel(channel)
                    if lane:
                        people=lane.members
                    if len(people)!=0:
                        for member in people:
                            try:
                                await member.move_to(bot.get_channel(TARGET))
                            except discord.Forbidden:
                                await bot.get_channel(BOTS_CHANNEL_ID).send(f"Can't move {member.display_name}")
                            except discord.HTTPException:
                                pass
                bot.timers[name]=None


bot.startTimers={"A":11*60,"B":11*60}
bot.timers={"A":None,"B":None}
bot.bootTime=time.time()//1
bot.version="0.4.2"

bot.faces={
    "big_eyes":["(◔ ◔)","(◔_◔)","◕⩊◕","◕ ◕","◉◉","◉ ◉","˵⊙ ⊙˵","˵⊙_⊙˵"],
    "question":["¯\\_(•᷄‎ n •́)_/¯?"],
    "love":[" ⸜(｡˃ ᵕ ˂ )⸝♡"],
    "happy":["^-^"],
    "blush_happy":["(⸝⸝> ᴗ•⸝⸝)"],
    "annoyed":["(⩌_⩌)","(⇀‸↼‶)","(•̀⤙•́ )","(｡•̀ ⤙ •́ ｡ꐦ) !!!","（ꐦ𝅒_𝅒）",">:T"],
    "pat":["( ⸝⸝´ ᵕ `⸝⸝)","(⸝⸝> ω <⸝⸝)","(⸝⸝0⸝⸝0⸝⸝)","(,,>﹏<,,)","( //>///<//)♡","♡.♡","♡^♡","♡_♡","♡V♡"],
    "tired":["(ᵕ —﹏—)","𖦹´ᯅ`𖦹","(╥﹏╥)","૮(◞ ‸ ◟)ა","(⩌_⩌)"],
    "concentrate":["(っ- ‸ - ς)"],
    "nervous":["(｡﹏｡\")","(•᷄- •᷅ ;)","(ᵕ ó ᴗ ò)","(•᷄ࡇ•᷅ ;)"],
    "sleep":["(ᴗ˳ᴗ)","૮˶- ﻌ -˶ა⌒)ᦱ","(_ _)。˚ ᶻ 𝘇 𐰁"]
}

bot.messageCD=60*60*0.1

BASE = Path(__file__).parent
bot.hotboot_file = BASE / "hotBoot.txt"
bot.restart_file = BASE / "restart.txt"
bot.user_data_path = BASE / "user_data.json"
bot.pause_file = BASE / "pauseTimes.txt"

bot.user_data=load_json(bot.user_data_path)

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))



