import datetime
import os
import json
import math
import random
from tkinter.messagebox import NO
from typing import Optional
from tkinter import Entry
from typing_extensions import Self
import asyncio
import discord
import typing
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix = '!', intents = intents)


#----------MEMBER JOIN AND LEAVE---------- BOT GOING ONLINE -----------------------------

@client.event

async def on_ready():

    print('Public Bot')


@client.event
async def on_member_join(member):
    guild = client.get_guild(1234) #<---- guild ID
    role = discord.utils.get(guild.roles, name="Member", id=1234)#<- role id and role name

@client.event

async def on_member_remove(member):

        print(f'{member} has left or was removed from {member.guild}')

#------------------------------------LOGs---------------------------------------------
@client.event
async def on_message_delete(message):
    embed=discord.Embed(title=f"{message.author.name} has deleted a message\nMessage deleted in {message.channel}", color=0xffff)
    embed.add_field(name= message.content ,value="This is the message that has been deleted", inline=True)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"ID: {message.author.id} ")
    channel=client.get_channel(1233)#<- log channel id
    await channel.send(embed=embed)


@client.event
async def on_message_edit(message_before, message_after):
    embed=discord.Embed(title=f"{message_before.author.name} edited a message\nMessage edited {message_before.channel}!", color=0xffff)
    embed.add_field(name= "Before" ,value= message_before.content, inline=False)
    embed.add_field(name= "After" ,value= message_after.content, inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"ID: {message_before.author.id}")
    channel=client.get_channel(1234)#log channel id
    await channel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):  # Requires Intents.reactions
    channel = client.get_channel(1234)#log channel id
    guild = client.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, id=1234)#log channel id

    if str(payload.emoji) == "👌":
        await payload.member.add_roles(role, atomic=True)

#------------------------------------Commands---------------------------------------------

@client.command()
async def timer(ctx, number:int):
    try:
        if number < 0:
            await ctx.send('number cant be a negative')
        elif number > 300:
            await ctx.send('number must be under 300')
        else:
            message = await ctx.send(number)
            while number != 0:
                number -= 1
                await message.edit(content=number)
                await asyncio.sleep(1)
            await message.edit(content='Ended!')

    except ValueError:
        await ctx.send('time was not a number')

@client.command()
async def poll(ctx, option1: str, option2: str, *, question):
  if option1==None and option2==None:
    ctx.send("You need to add another option...")
  elif option1==None:
    ctx.send("You need to add another option...")
  elif option2==None:
    ctx.send("You need to add another option...")
  else:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = {option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')

@client.command()
async def userinfo(ctx , member: discord.Member = None):

    date_format = "%a, %d %b %Y %I:%M %p"
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    member = ctx.author if not member else member
    roles = [role for role in member.roles if role.name != '@everyone']

    embed = discord.Embed(color=0xdfa3ff, description=member.mention)
    embed.set_author(name=str(member), icon_url=member.avatar.url)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Joined", value=member.joined_at.strftime(date_format))
    embed.add_field(name="Join position", value=str(members.index(member)+1))
    embed.add_field(name="Registered", value=member.created_at.strftime(date_format))
    if len(member.roles) > 1:
        role_string = ' '.join([r.mention for r in member.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        embed.set_footer(text='ID: ' + str(member.id))
        return await ctx.send(embed=embed)
      
        



@client.command(help = "Tells you how many bitches you get... - Made for John")
async def bitches(ctx):
    boi = ["0", "2", "3", "4", "5", "6", "7", "8", "9", "Too many for you to count!"]
    oi = ((random.choice(boi)))
    await ctx.send(f"You pull {oi} bitches!")

@client.command()
async def repeat(ctx, *, message):
    await ctx.send(message)
    await ctx.message.delete()

@client.command()
async def embed(ctx):
    questions = ["Title?", "Description?"]
    responses = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for question in questions:
        try:
            await ctx.send(question)
            message = await client.wait_for('message', timeout=15, check=check)

        except asyncio.TimeoutError:
            await ctx.send("Timeout")
            return

        else:
            responses.append(message.content)

    embedVar = discord.Embed(title=responses[0], description=responses[1])
    await ctx.send(embed=embedVar)

@client.command()
async def pug(ctx):
    await ctx.send('Bella Puggis Uggis Wuggis!')


@client.command()
async def ping(ctx):
    b=discord.Embed(title=f"Ping?!",description=f"Pong! {round(client.latency * 1000)}ms",color=0xFF5733)
    await ctx.send(embed=b)


@client.command(aliases=['8ball', 'test'])

async def _8ball(ctx,*, question):

    responses = ['It is certain',

                     'It is decidedly so',

                     'Without a doubt',

                     'Yes, definitely',

                     'You may rely on it',

                     'As I see it, yes',

                     'Most likely',

                     'Outlook good',

                     'Yes',

                     'Signs point to yes',

                     'Reply hazy try again',

                     'Ask again later',

                     'Better not tell you now',

                     'Cannot predict now',

                     'Concentrate and ask again',

                     'Do not count on it',

                     'My reply is no',

                     'My sources say no',

                     'Outlook not so good',

                     'Very doubtful']

    b=discord.Embed(title=f"The 8Ball Says!",description=f'Question: {question}\nAnswer: {random.choice(responses)}',color=0x660066)
    await ctx.send(embed=b)  


@client.command()

async def twitch(ctx):
        b=discord.Embed(title=f"The Twitch!",description="https://www.twitch.tv/Im2Slothy",color=0x6495ED)
        await ctx.send(embed=b)

@client.command(aliases=["mc"])

async def members(ctx):

    a=ctx.guild.member_count
    b=discord.Embed(title=f"Members in {ctx.guild.name}",description=a,color=discord.Color((0xffff00)))
    await ctx.send(embed=b)

#------------------------------------Moderation-------------------------------------------

@client.command()
async def unlock(ctx,):
    role = role or ctx.guild.default_role
    channel = channel or ctx.channel
    async with ctx.typing():
        if ctx.author.permissions_in(channel).manage_permissions:
            await ctx.channel.purge(limit=1)
            overwrite = channel.overwrites_for(role)
            overwrite.send_messages = True
            await channel.set_permissions(role, overwrite=overwrite)
            unlock_embed = discord.Embed(
            title= ("UNLOCKED"),
            description= (f"**{channel.mention}** HAS BEEN UNLOCKED FOR **{role}**"),
            colour=0x00FFF5,
            )        
            unlock_embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            unlock_embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            unlock_embed.set_thumbnail(url=ctx.guild.icon_url)    
            await ctx.channel.send(embed=unlock_embed, delete_after=10)
            print("unlock")
        else:
            error3_embed=discord.Embed(title="ERROR", description="YOU DONT HAVE PERMISSION", colour=0xff0000)
            error3_embed.set_thumbnail(url='https://images.emojiterra.com/google/android-11/512px/274c.png')
            error3_embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            error3_embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.channel.send(embed=error3_embed, delete_after=10)    

@client.command(description="Clears Chat!") # Kicks people
@commands.has_role('Moderator') #####<--- next bunch of commands change this to role needed for moderation
async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send('Messages have been cleared!')



@client.command(description="Kicks People!") # Kicks people

@commands.has_role('Moderator')

async def kick(ctx, member : discord.Member, *, reason=None):

        await member.kick(reason=reason)
        await ctx.sent(f'{member.mention} has been kicked!')




@client.command(description="Bans People!") # Bans people

@commands.has_role('Moderator')

async def ban(ctx, user: typing.Union[discord.Member, int], *, reason=None):
    guild = client.get_guild(1234)#guild id
    if user in ctx.guild.members:
        await user.ban(reason=reason)
        await ctx.send(f'Banned {user.mention}. That felt good.')
        #send banned user a message
        await user.send(f'You have been banned from {guild.name} for {reason}')
    else:
        await guild.ban(discord.Object(id = user))
        await ctx.reply(f'User has been hackbanned!\nUser: <@{user}>\nMy work here is done **Bombaclat!**')


@client.command(description="Unbans people!")

@commands.has_role('Moderator')

async def unban(ctx, *, member):

    obj = await commands.UserConverter().convert(ctx, member)

    if obj is None:

        id_ = await commands.IDConverter().convert(str(member))

        if id_ is not None:

            try:

                obj = await client.fetch_user(int(id_.group(1)))

            except discord.NotFound:

                obj = None

        if obj is None:

            await ctx.send('User not found')

            return 

    await ctx.guild.unban(obj)

    await ctx.send(f'Unbanned {obj}')


@client.command(description="Mutes the specified user.") # Mutes user non timed
@commands.has_role('Moderator')
async def mute(ctx, member: discord.Member, time, reason=None):
    desctime = time
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    time_convert = {"s":1, "m":60, "h":3600, "d":86400}
    tempmute= int(time[:-1]) * time_convert[time[-1]]
    if not mutedRole:
        mutedRole = discord.utils.get(guild.roles, name="MUTED", id=786237913217105931)
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted for {desctime} ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=True)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await asyncio.sleep(tempmute)
    await member.send(f"You have been muted from: {guild.name} reason: {reason}")
    await member.remove_roles(mutedRole)

client.run("TOKEN")
