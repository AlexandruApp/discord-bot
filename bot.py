import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import os
from discord.utils import get
import random, youtube_dl

client = commands.Bot(command_prefix = '/')

@client.event
async def on_ready():
    print('Bot is online')

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} ms')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Nigga I'll leave {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")

@client.command(pass_context=True, aliases=['tell-wisdom', 'tell wisdom'])
async def tell_wisdom(ctx):
    wisdom = ["You gay", "You also gay", "Y are you losing your time with this?", "I wanna die", "Geneva Convention.More like Geneva sugestion.", "Hitler was a great man!", "I like egg salad"]
    await ctx.send(random.choice(wisdom))


@client.command(pass_context=True)
async def play_song(ctx):
    await ctx.channel.purge(limit=1)
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 20

@client.command(pass_context=True)
async def stop(ctx):
    await ctx.channel.purge(limit=1)
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        print("Bot stoped")
    else:
        print("Bot is already stoped")

@client.command(pass_context=True)
async def kick_all(ctx):
    await ctx.send("Kicking all users in 1h.Save any important files now.")
    await ctx.send("Tic toc.. tic toc..")

@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    await ctx.channel.purge(limit=1)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)


    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1

    nname = name.rsplit("-", 2)
    # await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
client.run('NzA0MzA4NjM3MTU3NDI1MjQ1.XqbQwA.QB0OPonnaeCU_qXcxft_fbNDkO8')