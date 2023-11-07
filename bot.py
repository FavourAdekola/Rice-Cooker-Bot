import discord
import responses
import datetime
import random
from asyncio import run_coroutine_threadsafe
from discord.ext import commands
import json
import re
from urllib import parse, request
import os
import asyncio
from youtube_dl import YoutubeDL
from music_cog import music_cog
from info import TOKEN

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response)  if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.all()
    intents.message_content = True

    bot = commands.Bot(command_prefix='cook ', intents = intents)

    

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        await bot.change_presence(activity=discord.Game("Cooking Rice"))
        await bot.add_cog(music_cog(bot))

        # It's The First Of The Month
        day = datetime.datetime.now()
        if day.strftime("%d") == "01":
            print("It's the first of the month")
            await bot.get_channel(698008492526665780).send("https://cdn.discordapp.com/attachments/1046948327767412816/1048005776318414919/263521927_1036371346932224_1220958437198197236_n.mp4")
        if day.strftime("%A") == "Friday":
            print("It's Friday")
            choice = random.choice([1,2])
            if choice == 1:
                await bot.get_channel(698008492526665780).send("https://cdn.discordapp.com/attachments/1046948327767412816/1048347906706513930/yt5s.com-ITS_YAKUZA_FRIDAY360p.mp4")
            if choice == 2:
                await bot.get_channel(698008492526665780).send("https://cdn.discordapp.com/attachments/1046948327767412816/1048349749679501424/yt5s.com-Today_is_Friday_in_California360p.mp4")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        await bot.process_commands(message)
        await send_message(message,user_message, is_private=False )


    
    bot.run(TOKEN)