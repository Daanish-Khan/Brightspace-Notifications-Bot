#!/brightspacenotifs/bin/python3

import discord
import threading
import gmail_reader
import re
import json
from datetime import datetime

import html

from helper import helper
from discord.ext import commands, tasks


bn = commands.Bot(command_prefix="-")
gr = gmail_reader.gmail_reader("brightspacenotifs@gmail.com", "EECS2020", "Inbox")
token = "NzYwMzA2MDYyNDM1Mjg3MDQw.X3KIMw.gazV3KLA2q0f2ENhHLMKGy1dYMY"
thread = None

h = helper()

channeldict = {}


def reset():
    gr = gmail_reader.gmail_reader("brightspacenotifs@gmail.com", "EECS2020", "Inbox")


@tasks.loop(seconds=1)
async def check_timeout(thread):

    if h.get_timeout_flag():

        print("Stopping listener...")
        gr.logout()
        thread.join()

        print("Starting listener...")
        reset()
        thread = threading.Thread(target=gr.listen_to_messages, args=[60, h])
        thread.start()

        h.set_timeout_flag(False)


@tasks.loop(seconds=1)
async def process_message(ctx):
    global message

    if len(h.get_message()) != 0:

        jsondict = json.loads(h.get_message().pop())

        title = jsondict["Subject"]

        if "announcements" in title.lower():
            body = re.findall(r'<p>(.*?)</p>', jsondict["Plain_Text"])
            body = ["\r\n" if x == '' else x for x in body]

            i = 0
            while i < len(body):
                body.insert(i, '\r\n')
                i += 2

            body = " ".join(body)
            body = html.unescape(re.sub("<.*?>", "", body))

        elif "assignments" in title.lower():
            body = re.findall(r'<div style="margin:0px;padding:0px;color:#000000;">(.*?)</div>', jsondict["Plain_Text"])
            body = html.unescape(body[0])

        for key in channeldict:
            if key in title:
                time = datetime.now()
                time = time.strftime("%H:%M")

                embed = h.embed_builder(key, title, body, time)
                await ctx.guild.get_channel(channeldict[key]).send(embed=embed)


@bn.event
async def on_ready():
    gr.login()
    print("Ready!")


@bn.command(aliases=["listen"])
@commands.has_role("BIG DADDY MOD")
async def start_listening(ctx):

    thread = threading.Thread(target=gr.listen_to_messages, args=[60, h])
    thread.start()

    process_message.start(ctx)
    check_timeout.start(thread)
    await ctx.send("I will now start listening for emails!")


@bn.command()
@commands.has_role("BIG DADDY MOD")
async def close(ctx):
    await ctx.send("I am no longer listening to emails!")
    await bn.close()
    gr.logout()
    print("Bot Closed")


@bn.command(aliases=["addclass"])
@commands.has_role("BIG DADDY MOD")
async def add_notif_channel(ctx, class_name):
    if class_name in channeldict:
        await ctx.send(f'{class_name} is already registered.')
    else:
        channeldict[class_name] = ctx.message.channel.id
        await ctx.send(f'{class_name} has been registered for channel {ctx.message.channel.mention}!')


@bn.command(aliases=["removeclass"])
@commands.has_role("BIG DADDY MOD")
async def remove_notif_channel(ctx, class_name):
    if class_name in channeldict:
        channeldict.pop(class_name)
        await ctx.send(f'{class_name} has been removed for this channel!')
    else:
        await ctx.send(f'{class_name} has not been registered.')


@bn.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bn.latency * 1000)}ms')


bn.run(token)
