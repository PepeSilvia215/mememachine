import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import glob

#commonly used values
prefix = "##"
#status = "potatoe.exe"

#helper functions
def getapikey():
    api_key_file = open("api-key", "r")
    api_key = api_key_file.readline()
    api_key_file.close()
    return api_key

def findmemes(query, numresults):
    memefiles = getmemefiles()
    matches = [k for k in memefiles if query in k]
    return matches[:numresults]

def getmemefiles():
    memefiles = []
    for file in glob.glob("muh_sounds_bruh/**/*.flac", recursive=True):
            file = file[len("muh_sounds_bruh/"):]
            file = file[:-(len(".flac"))]
            memefiles.append(file)
    memefiles.sort()
    return memefiles 

#async def messagehim(text):
#    await bot.send_message(discord.Object(id=
#print("*begins screeching*")
#end helper functions

#begin bot, actual things start to happen here
print("*begins screeching*")
#write process pid to die file
if os.path.exists("idontwannadie"): #if die file exists
    os.remove("idontwannadie") #destroy it
pid = os.getpid()
print("muh' pid is " + str(pid))
fout = open("idontwannadie", "wt")
fout.write(str(pid))
fout.close()
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
#    await bot.change_presence(game=discord.Game(name=status))
    print("bruh we made it we " + bot.user.name + "#" + bot.user.discriminator)
#    await messagehim("MemeMachine up and running like a dream bruh")

#commands
@bot.command(brief="plays the requested meme bruh", description="will play the meme in muh sounds bruh that exactly matches")
async def play(self, context, *args):
    message = context.message
    if not args:
        await message.channel.send("bruh i need a meme to play")
        return
    meme = args[0]
    #check if they are in a voice channel first
    voice_channel=user.voice.voice_channel
    if(voice_channel == None):
        await message.channel.send("bruh you gotta be in a voice channel first")
        return
    #find the meme
    meme = findmemes(meme, 1)[0]
    if(meme == []):
        await message.channel.send("no meme bruh")
        return
    memepath = "/home/pepesilvia/mememachine/muh_sounds_bruh/" + meme + ".flac"
    #await message.channel.send("i wanna play " + memepath)
    #create StreamPlayer
    vc = await bot.join_voice_channel(voice_channel)
    player = vc.create_ffmpeg_player(memepath, after=lambda: print("done playing " + memepath))
    print("playing " + memepath)
    player.start()
    while not player.is_done():
        await asyncio.sleep(1)
    #disconnect when done
    player.stop()
    await vc.disconnect

@bot.command(brief="kills me bruh pls dont", description="bruh pls bruh i dont wanna die bruh\nto kill me you have to use my pid found in the `idontwannadie` file or printed out when i was born\nnot for normies")
async def kys(self, context, *args):
    message = context.message
    if not args:
        await message.channel.send("you think you can kill me? normies cant kill me bruh you gotta use muh pid")
        return
    password = args[0]
    if password == str(pid):
        print("recieved kill command, sepeku time")
        await bot.close()

@bot.command(brief="returns the integer id for your user bruh", description="returns the integer id for your user bruh, useful for discord debug n shit")
async def getid(self, context):
    message = context.message
    await message.author.send(str(message.author.id))

@bot.command(brief="search and find up to 25 memes bruh", description="shows the first 25 memes that contain substrings that exactly match bruh")
async def search(self, context, *args):
    message = context.message
    if not args:
        await context.channel.send("try using a search term bruh")
        return
    query = args[0]
    matches = findmemes(query, 25)
    if(matches == []):
        await message.channel.send("no sounds bruh")
    else:
        matches.insert(0, "")
        searchmessage = "\n".join(matches)
        await message.channel.send("bruh are you lookin for ```" + searchmessage + "```") 

@bot.command(brief="sends you all the memes in a massive DM, dont", description="this will tear into your DMs and send you all the available memes, which is so many memes bro. to actually send all the memes use\n##list memes\nthis is done to prevent your destruction")
async def list(self, context, *args):
    message = context.message
    if not args:
        if not args[0] == "memes":
            await message.channel.send("bruh i am so full of memes, if you are sure you want this use `##list memes`")
            return
    elif(password == "memes"):
        await message.author.send("here are the available memes:")
        memefiles = getmemefiles()
        #split into chunks
        chunksize = 50
        chunks = [memefiles[i:i + chunksize] for i in range(0, len(memefiles), chunksize)]
        for memefileschunk in chunks:
            mememessage = "\n".join(memefileschunk)
            await message.author.send(mememessage)
        await message.channel.send("you will not survive")

@bot.command(brief="prints this message bruh", description="bruh dont you have something better to be doin")
async def help(self, context, *args):
    message = context.message
    if not args:
        pass
        #print normal help message
    command = args[0]
    #print help message based on command
#end commands

@bot.event
async def on_message(message):
    #ignore messages from muh' self
    if message.author == bot.user:
        return
    #insert a cheeky lil quote if its the help message
    if message.content.startswith("##help"):
        await message.channel.send("_\"My guess is that you've been confused for a very long time.\"_")
    #process commands
    await bot.process_commands(message)

bot.run(getapikey(), bot=True)
