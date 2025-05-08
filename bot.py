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
from yt_dlp import YoutubeDL
from music_cog import music_cog
from info import TOKEN

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if response != "https://tenor.com/view/rizz-hoop-peter-griffin-green-fn-gif-16271132247808270949":
            await message.author.send(response)  if is_private else await message.channel.send(response)
        else:
            await message.author.send(response, delete_after=5) if is_private else await message.channel.send(response, delete_after=5)
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
        # Start a background task that checks daily events
        bot.loop.create_task(daily_message_checker(bot))

        # It's The First Of The Month
        """ day = datetime.datetime.now()
        if day.strftime("%d") == "01":
            print("It's the first of the month")
            await bot.get_channel(698008492526665780).send("https://cdn.discordapp.com/attachments/1046948327767412816/1048005776318414919/263521927_1036371346932224_1220958437198197236_n.mp4")
        if day.strftime("%A") == "Friday":
            print("It's Friday")
            choice = random.choice([1,2])
            if choice == 1:
                await bot.get_channel(698008492526665780).send("https://cdn.discordapp.com/attachments/1046948327767412816/1048347906706513930/yt5s.com-ITS_YAKUZA_FRIDAY360p.mp4")
            if choice == 2:
                await bot.get_channel(698008492526665780).send("https://cdn.discordapp.com/attachments/1046948327767412816/1048349749679501424/yt5s.com-Today_is_Friday_in_California360p.mp4") """


    async def daily_message_checker(bot):
        posted_today = {"first_of_month": False, "friday": False}
        channel_id = 698008492526665780  # Replace with your actual channel ID

        while True:
            now = datetime.datetime.now()

            # Reset at midnight
            if now.hour == 0 and now.minute == 0:
                posted_today = {"first_of_month": False, "friday": False}

            # First of the month
            if now.day == 1 and not posted_today["first_of_month"]:
                print("Posting first of the month message")
                channel = bot.get_channel(channel_id)
                await channel.send("https://cdn.discordapp.com/attachments/1046948327767412816/1048005776318414919/263521927_1036371346932224_1220958437198197236_n.mp4")
                posted_today["first_of_month"] = True

            # Friday message
            if now.strftime("%A") == "Friday" and not posted_today["friday"]:
                print("Posting Friday message")
                channel = bot.get_channel(channel_id)
                choice = random.choice([1, 2])
                if choice == 1:
                    await channel.send("https://cdn.discordapp.com/attachments/1046948327767412816/1048347906706513930/yt5s.com-ITS_YAKUZA_FRIDAY360p.mp4")
                else:
                    await channel.send("https://cdn.discordapp.com/attachments/1046948327767412816/1048349749679501424/yt5s.com-Today_is_Friday_in_California360p.mp4")
                posted_today["friday"] = True

            await asyncio.sleep(60)  # Wait 1 minute before checking again

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        await bot.process_commands(message)
        
        await send_message(message,user_message, is_private=False )


    @bot.command(name="delete")
    async def delete(ctx: commands.Context, *,num: int):

        if ctx.message.author.guild_permissions.manage_messages and num <= 100:
            await ctx.channel.purge(limit = num +1)
            await ctx.send(f"Deleted {num} messages.", delete_after=5)
        else:
            await ctx.send("You can't do that! :shushing_face: :deaf_person: ")

    @bot.command(name="mog")
    async def mogging(ctx: commands.Context):
        await ctx.send(":shushing_face: :deaf_person:")



    
    bot.run(TOKEN)