import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import time
import random
from pathlib import Path
import platform

from data_manage import save_json, load_json, load_txt
"""
load_txt returns a list of str from the filepath
load_json and save_json loads from and saves to json files

neither does anything else other than open the file on the filepath and load the data from it
"""

class Item:
    def __init__(self,type:str,tier:int,name:str):
        self.tier=tier
        self.type=type
        self.name=name

class Button(discord.ui.View):
    @discord.ui.button(label="Click Me", style=discord.ButtonStyle.primary)
    async def button_callback(self,interaction: discord.Interaction,button: discord.ui.Button):
        #await interaction.response.send_message("Button!",ephemeral=True) #only clicker sees
        await interaction.response.send_message("Button!")

class MultButton(discord.ui.View):
    def __init__(self, author: discord.User):
        super().__init__(timeout=60)  #expire in 60 sec
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id!=self.author.id:
            await interaction.response.send_message("You can't use these buttons.",ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="1", style=discord.ButtonStyle.success)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message("1!")
        
    @discord.ui.button(label="2", style=discord.ButtonStyle.danger)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message("2!")


class FindRem(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)  #expire in 60 sec
        self.ctx = ctx
        self.author = ctx.author
        
        self.buttonTexts=[]
        for i in range(9):
            if random.randint(0,2)==0:
                self.buttonTexts.append("Nothing\nBut money!")
            else:
                self.buttonTexts.append("Nothing...")
        rRem=random.randint(0,8)
        self.buttonTexts[rRem]=":blue_circle: :blue_circle:\nA lot of money!\n"
        rBird=random.randint(0,8)
        rBird2=random.randint(0,4)
        if rBird%4==rBird2 and rRem!=rBird:
            self.buttonTexts[rBird]="OH oh...\n:green_circle::owl:\n"
        
        posibleLabels=[
            "yellow walker",
            "yellow guardian",
            "blue walker",
            "blue guardian",
            "green walker",
            "green guardian",
            "yellow sinner",
            "green sinner",
            "blue left sinner",
            "blue right sinner",
            "enemy double sinner",
            "friendly double sinner",
            "yellow secret shop",
            "green secret shop",
            "midboss",
            "yellow bridgebuff",
            "green bridgebuff",
            "yellow teleporter",
            "green teleporter"
        ]
        self.labels=[]
        for i in range(9):
            r=random.randint(0,len(posibleLabels)-1)
            self.labels.append(posibleLabels[r])
            posibleLabels.pop(r)
        self.button1.label = self.labels[0]
        self.button2.label = self.labels[1]
        self.button3.label = self.labels[2]
        self.button4.label = self.labels[3]
        self.button5.label = self.labels[4]
        self.button6.label = self.labels[5]
        self.button7.label = self.labels[6]
        self.button8.label = self.labels[7]
        self.button9.label = self.labels[8]

    def resoultEval(self,buttonText):
        authorID=str(self.author.id)
        if ":blue_circle:" in buttonText:
            r=random.randint(4,10)
            bot.user_data[authorID]["money"]["unsecured"]+=r*100
            return ("The Rem gave you "+str(r*100)+" souls.")
        elif buttonText=="Nothing\nBut money!":
            r=random.randint(1,3)
            bot.user_data[authorID]["money"]["secured"]+=r*100
            return ("You got "+str(r*100)+" souls.")
        elif ":green_circle::owl:" in buttonText:
            moneyLost=bot.user_data[authorID]["money"]["unsecured"]
            bot.user_data[authorID]["money"]["unsecured"]=0
            return ("You died and lost "+str(moneyLost)+" unsecured souls.")
        return ""

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id!=self.author.id:
            await interaction.response.send_message("You can't use these buttons.",ephemeral=True)
            return False
        return True
    
    #, emoji=""

    @discord.ui.button(label="1", style=discord.ButtonStyle.primary,row=0)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[0]+"\n"+self.resoultEval(self.buttonTexts[0]))
        
    @discord.ui.button(label="2", style=discord.ButtonStyle.primary,row=0)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[1]+"\n"+self.resoultEval(self.buttonTexts[1]))
        
    @discord.ui.button(label="3", style=discord.ButtonStyle.primary,row=0)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[2]+"\n"+self.resoultEval(self.buttonTexts[2]))

        
    @discord.ui.button(label="4", style=discord.ButtonStyle.primary,row=1)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[3]+"\n"+self.resoultEval(self.buttonTexts[3]))
        
    @discord.ui.button(label="5", style=discord.ButtonStyle.primary,row=1)
    async def button5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[4]+"\n"+self.resoultEval(self.buttonTexts[4]))
        
    @discord.ui.button(label="6", style=discord.ButtonStyle.primary,row=1)
    async def button6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[5]+"\n"+self.resoultEval(self.buttonTexts[5]))
        
        
    @discord.ui.button(label="7", style=discord.ButtonStyle.primary,row=2)
    async def button7(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[6]+"\n"+self.resoultEval(self.buttonTexts[6]))
        
    @discord.ui.button(label="8", style=discord.ButtonStyle.primary,row=2)
    async def button8(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[7]+"\n"+self.resoultEval(self.buttonTexts[7]))
        
    @discord.ui.button(label="9", style=discord.ButtonStyle.primary,row=2)
    async def button9(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.send_message(self.buttonTexts[8]+"\n"+self.resoultEval(self.buttonTexts[8]))


#users
ME=616710497378631709
BOT_ROLE=1516075439347470437

#channel(s)
BOTS_CHANNEL_ID = 1515333724269445270


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

def loadItemsProper(items):
    newItems=[]
    for curItem in items:
        curItemParts=curItem.split(" ")
        newItems.append(Item(curItemParts[0],int(curItemParts[1]),curItemParts[2]))
    return newItems

def activeTimerExists():
    for i, (timerName,timerTime) in enumerate(bot.timers.items()):
        if timerTime!=None:
            return True
    return False


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
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
            await bot.get_channel(BOTS_CHANNEL_ID).send("I'm awake!\nGood morning!\n"+face)
        else:
            await bot.get_channel(BOTS_CHANNEL_ID).send("Back online! "+face)

    if not tick.is_running():
        tick.start()

@bot.event
async def on_message(message):
    if message.author.bot or message.webhook_id is not None or message.author == bot.user:
        return
    idSTR=str(message.author.id)
    if message.reference:
        repliedTo=await message.channel.fetch_message(message.reference.message_id)
        if repliedTo.author.id == bot.user.id:
            thankingMessages=["thank you!","thank you","thanks!","thanks"]
            if message.content.lower() in thankingMessages:
                if "My brain" in repliedTo.content:
                    await message.reply("You're welcome!\n"+chooseFaceFromCategory("brain_hurt"))
                else:
                    await message.reply("You're welcome!\n"+chooseFaceFromCategory("pat"))
    if str(message.author.id) not in bot.user_data.keys():
        bot.user_data[idSTR]={}
        bot.user_data[idSTR]["main"]="None"
        bot.user_data[idSTR]["steamID"]="None"
        bot.user_data[idSTR]["steamID3"]="None"
        bot.user_data[idSTR]["steamID64"]="None"
        bot.user_data[idSTR]["money"]={}
        bot.user_data[idSTR]["money"]["unsecured"]=0
        bot.user_data[idSTR]["money"]["secured"]=0
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
                        users_in_voice.append(str(member.id)+" in "+voice_channel.name)
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
            bot.user_data[idSTR]["money"]["unsecured"]+=100+random.randint(0,lenght)*bonusM
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
            #await ctx.send("TEST:\nNothing to test.\n.=.",delete_after=10)
            view=Button()
            view=MultButton(ctx.author)
            view=FindRem(ctx)
            await ctx.send("Buttons:", view=view)

@bot.command()
async def minigames(ctx, game:str=None):
    senderID=ctx.author.id
    if ctx.channel.id == BOTS_CHANNEL_ID:
        if game==None:
            games=[
                "`!minigames find_Rem`: Try to find the enemy Rem and stop them from getting the sinners.",
            ]
            await ctx.reply('\n'.join(games))
        elif game=="find_Rem":
            view = FindRem(ctx)
            print(view.buttonTexts)
            await ctx.reply("Find the enemy Rem:", view=view)

@bot.command()
async def start(ctx):
    senderID=ctx.author.id
    if ctx.channel.id == BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel to be able to start a timer.")
            else:
                if bot.timers[ctx.author.voice.channel.category.name[-2]]==None:
                    bot.timers[ctx.author.voice.channel.category.name[-2]]=time.time()+bot.startTimers[ctx.author.voice.channel.category.name[-2]]
                    await ctx.reply("Started timer for the ["+ctx.author.voice.channel.category.name[-2]+"] category.")
                    
                    name=ctx.author.voice.channel.name[-2]
                    names=[]
                    for guild in bot.guilds:
                        for channel in discord.utils.get(guild.categories, name="["+name+"]").voice_channels:
                            for member in channel.members:
                                if member.global_name=="PurpleEarthDragon":
                                    names.append(member.global_name+chooseFaceFromCategory("love"))
                                else:
                                    names.append(member.global_name)
                    
                    await ctx.send("__Good luck, and Have fun!__\n"+'\n'.join(names)+"\n"+chooseFaceFromCategory("happy"),delete_after=bot.startTimers[ctx.author.voice.channel.category.name[-2]])
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
            if activeTimerExists():
                ctx.reply("Sorry, I can't shutdown now, there is at least 1 active timer.")
            else:
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
            if activeTimerExists():
                ctx.reply("Sorry, I restart now, there is at least 1 active timer.")
            else:
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
            if activeTimerExists():
                await ctx.reply("Sorry, I can't go to sleep now, there is at least 1 active timer.")
            else:
                if ctx.guild.voice_client:
                    await ctx.guild.voice_client.disconnect()
                if save=="save":
                    save_json(bot.user_data_path,bot.user_data)
                
                with open(bot.restart_file,"w") as f:
                    f.write("2")
                with open(bot.pause_file,"r") as f:
                    pauseStart=f.readline().strip()
                    pauseEnd=f.readline().strip()
                
                await ctx.reply("Going to sleep\nI will be unavailable between "+pauseStart+" and "+pauseEnd+" CEST\n"+chooseFaceFromCategory("sleep"),delete_after=20)
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
                await ctx.reply("Starting time set to "+str(x)+" minutes.")
            
@bot.command()
async def gettimer(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.author.voice==None:
                await ctx.reply("You must be in a voice channel to view a timer lenght.")
            else:
                await ctx.reply("The timer is set to "+str(bot.startTimers[ctx.author.voice.channel.category.name[-2]]/60)+" minutes.")

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
                "`!bot_help data`: Commands about a minigame that is in development.",
                "`!bot_help tools`: Commands about some 'tools' and tools I can provide to spice up your game.",
                "`!bot_help extra`: Commands about no particular topic.",
            ]
        elif section=="timer":
            anyView=True
            botcommands=[
                "`!start` and `!start second`: Start an x minute timer. When the timer ends I put everyone into the `Deadlock [#]` channel (from lane channels).\n(Timer lenght is configureable; only 1 timer can be used at the same time (as right no there is only 1 set of lane channels))",
                "`!end`: Ends the timer and moves everyone immediately.",
                "`!endit`: Ends the timer without sending people to the `Deadlock [#]` channel.",
                "`!settimer x`: Set the timer lenght to x minutes.",
                "`!gettimer`: Tells you the timer lenght.",
                "`!remaining:` Tells you how much time remains on the timer.",
            ]
        elif section=="voice":
            face=chooseFaceFromCategory("annoyed")
            anyView=True
            botcommands=[
                "`!join`: I will join `Deadlock [#]` and will use an experimental feature to automate my timer functionality.",
                "`!leave`: I will leave `Deadlock [#]` but will contionue counting for the timer.",
                "(feature is not possible "+face+", but I can be there for emotional support."
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
        elif section=="data":
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
                "`!minigame`: Play some games while you wait for matchmaking.",
                "`!source`: Lobotomy (source code)"
            ]
        elif section=="tools":
            anyView=True
            botcommands=[
                "`!rand X Y`: All sorts of randomly given stuff. (use `!rand` to learn more)"
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
                    await ctx.reply("Remaining time: "+str(round(abs(bot.timers[ctx.author.voice.channel.category.name[-2]]-time.time())/60,2))+" min(s).")
                else:
                    await ctx.reply("Timer is not active.")

@bot.command()
async def status(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME:
            face=chooseFaceFromCategory("annoyed")
            l="."
            for i in face:
                l+=" "
            l+="(Why do you want to know?)"
            await ctx.reply(l+"\n"+face)
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
            extra="\nI'm tired. "+chooseFaceFromCategory("tired")
        await ctx.reply("Bot version: "+bot.version+"\nOS:"+winlin+"\nHardware I'm living on:"+cpu+"\nI've been running for: "+str(hours)+" hours, "+str(minutes)+" minutes and "+str(seconds)+" seconds."+extra)
        if lindistr!=None:
            await ctx.send("Fun fact: Most likely I'm running on a rasberry pi 5. :D\nLinux dist: "+lindistr["PRETTY_NAME"],delete_after=30)

@bot.command()
async def join(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            if ctx.guild.voice_client!=None:
                await ctx.reply("Sorry I'm busy in another channel. "+chooseFaceFromCategory("nervous"))
            else:
                if ctx.author.voice==None:
                    await ctx.reply("You must be in a voice channel so I know which channel to join.")
                else:
                    channel = ctx.author.voice.channel
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
        character=bot.characters
        if main in character:
            bot.user_data[str(senderID)]["main"]=main
            await ctx.reply("You set your main to: "+main)
        else:
            await ctx.reply("That is not a valid character.")

@bot.command()
async def set_steam_id(ctx,id:int):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        bot.user_data[str(senderID)]["steamID"]=str(id)
        ctx.reply("I will remember your steam ID"+chooseFaceFromCategory("evil"))

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
            if isinstance(data,dict):
                inData=""
                for j, (innerKey,innerData) in enumerate(data.keys()):
                    inData+=innerKey+": "+innerData+"\n"
                message+=key+":\n\t"+inData+"\n"
            else:
                message+=key+": "+data+"\n"
        await ctx.reply(message,delete_after=10)
        
@bot.command()
async def remove_me(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        bot.user_data[str(senderID)]={
            "main":"None",
            "steamID":"None",
            "steamID3":"None",
            "steamID64":"None",
            "money":{"unsecured":0,"secured":0},
            "items":[],
            "lvl":0,
            "XP":0
        }
        if random.randint(0,1)==0:
            face=chooseFaceFromCategory("nervous")
        else:
            face=chooseFaceFromCategory("question")
        await ctx.reply("Who are you?\n"+face)

@bot.command()
async def save(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME or any(role.id == BOT_ROLE for role in ctx.author.roles):
            save_json(bot.user_data_path,bot.user_data)
            await ctx.reply("Saving some stuff. "+chooseFaceFromCategory("concentrate"),delete_after=10)

@bot.command()
async def clear_loaded(ctx):
    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if senderID==ME:
            bot.user_data={}
    await ctx.reply("I forgor. Head empty...\n"+chooseFaceFromCategory("big_eyes"))

@bot.command()
async def rand(ctx,sub:str=None, num:int=1):
    def getItemsType(items,type:str):
        returnItems=[]
        for curItem in items:
            if curItem.type==type:
                returnItems.append(curItem)
        return returnItems
    def getItemsTier(items,tier:int):
        returnItems=[]
        for curItem in items:
            if curItem.tier==tier:
                returnItems.append(curItem)
        return returnItems

    senderID=ctx.author.id
    if ctx.channel.id==BOTS_CHANNEL_ID:
        if sub==None:
            botcommands=[
                "`!rand char X`: Generates X random characters. (1 to 12)",
                "`!rand char_pair X`: Generates X random character pairs. To play with a friend. (1 to 6)",
                "`!rand item X`: Generates X random items. (1 to number of items)",
                "`!rand item_gun X`: Generates X random gun items. (1 to number of gun items)",
                "`!rand item_vit X`: Generates X random vitality items. (1 to number of vitality)",
                "`!rand item_spi X`: Generates X random spirit items. (1 to number of spirit items)",
                "`!rand item_tierI X`: Generate X random items from tier I. (1 to number of tier I items)",
                "`!rand item_tierII X`: Generate X random items from tier II. (1 to number of tier II items)",
                "`!rand item_tierIII X`: Generate X random items from tier III. (1 to number of tier III items)",
                "`!rand item_tierIV X`: Generate X random items from tier IV. (1 to number of tier IV items)",
            ]
            await ctx.reply('\n'.join(botcommands))
        elif sub=="char":
            returnChars=""
            oChars=bot.characters.copy()
            if num<1:
                num=1
            elif num>12:
                num=12
            for i in range(num):
                r=random.randint(0,len(oChars))
                returnChars+=oChars[r]+"\n"
                oChars.pop(r)
            await ctx.reply(returnChars)
        elif sub=="char_pair":
            returnChars=""
            oChars=bot.characters.copy()
            if num<1:
                num=1
            elif num>6:
                num=6
            for i in range(num):
                smallList=""
                r=random.randint(0,len(oChars))
                smallList+=oChars[r]+"; "
                oChars.pop(r)
                r=random.randint(0,len(oChars))
                smallList+=oChars[r]
                oChars.pop(r)
                returnChars+=smallList+"\n"
            await ctx.reply(returnChars)
        elif sub=="item":
            returnChars=""
            oItems=bot.items.copy()
            if num<1:
                num=1
            elif num>len(oItems):
                num=len(oItems)
            for i in range(num):
                r=random.randint(0,len(oItems))
                returnChars+=oItems[r].name.replace("_"," ")+"\n"
                oItems.pop(r)
            await ctx.reply(returnChars)
        elif sub=="item_gun":
            returnChars=""
            oItems=getItemsType(bot.items,"gun")
            if num<1:
                num=1
            elif num>len(oItems):
                num=len(oItems)
            for i in range(num):
                r=random.randint(0,len(oItems))
                returnChars+=oItems[r].name.replace("_"," ")+"\n"
                oItems.pop(r)
            await ctx.reply(returnChars)
        elif sub=="item_vit":
            returnChars=""
            oItems=getItemsType(bot.items,"vitality")
            if num<1:
                num=1
            elif num>len(oItems):
                num=len(oItems)
            for i in range(num):
                r=random.randint(0,len(oItems))
                returnChars+=oItems[r].name.replace("_"," ")+"\n"
                oItems.pop(r)
            await ctx.reply(returnChars)
        elif sub=="item_spi":
            returnChars=""
            oItems=getItemsType(bot.items,"spirit")
            if num<1:
                num=1
            elif num>len(oItems):
                num=len(oItems)
            for i in range(num):
                r=random.randint(0,len(oItems))
                returnChars+=oItems[r].name.replace("_"," ")+"\n"
                oItems.pop(r)
            await ctx.reply(returnChars)
        elif "item_tierI" in sub:
            returnChars=""
            if sub=="item_tierIV":
                oItems=getItemsTier(bot.items,4)
            else:
                oItems=getItemsTier(bot.items,sub.count("I"))
            if num<1:
                num=1
            elif num>len(oItems):
                num=len(oItems)
            for i in range(num):
                r=random.randint(0,len(oItems))
                returnChars+=oItems[r].name.replace("_"," ")+"\n"
                oItems.pop(r)
            await ctx.reply(returnChars)
        else:
            await ctx.reply("I can't give you a random thing in that category."+chooseFaceFromCategory("nervous"))




@tasks.loop(seconds=1)
async def tick():
    for i, (name,timerTime) in enumerate(bot.timers.items()):
        if timerTime!=None:
            curTime=time.time()//1
            timerTime=timerTime//1
            if timerTime-curTime==60:
                await bot.get_channel(BOTS_CHANNEL_ID).send("1 minute remaining on the ["+name+"] timer.",delete_after=60)
            elif timerTime<=curTime:
                await bot.get_channel(BOTS_CHANNEL_ID).send("Moving people in category ["+name+"].",delete_after=60)
                for guild in bot.guilds:
                    category = discord.utils.get(guild.categories, name="["+name+"]")
                    TARGET=discord.utils.get(category.voice_channels, name="Deadlock ["+name+"]").id
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
                                await bot.get_channel(BOTS_CHANNEL_ID).send("Can't move "+member.display_name)
                            except discord.HTTPException:
                                pass
                bot.timers[name]=None


bot.startTimers={"A":11*60,"B":11*60}
bot.timers={"A":None,"B":None}
bot.bootTime=time.time()//1
bot.version="0.5.3"



bot.messageCD=60*60*0.1 #6 minutes

BASE = Path(__file__).parent
bot.hotboot_file = BASE / "hotBoot.txt"
bot.restart_file = BASE / "restart.txt"
bot.user_data_path = BASE / "user_data.json"
bot.pause_file = BASE / "pauseTimes.txt"

bot.characters_file = BASE / "characters.txt"
bot.items_file = BASE / "items.txt"

bot.face_file = BASE / "faces.json"

bot.faces=load_json(bot.face_file)
bot.user_data=load_json(bot.user_data_path)

bot.characters=load_txt(bot.characters_file)

bot.items=loadItemsProper(load_txt(bot.items_file))

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))



