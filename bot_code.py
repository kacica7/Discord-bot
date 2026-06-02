import discord
from discord.ext import commands
from PIL import Image
import aiohttp
import io
import os
import random

TOKEN = 'token'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = '!', intents = intents)

#dictionary that stores the meme images; the numbers represent the coordinates of the
#avatar, width and height
MEMES = {

    "coding_me.jpg" : (100, 100, 150, 150),
    'computer_science.png' : (150, 120, 130, 130),
    'kalm.jpg' : (80, 180, 160, 160),
    'oop.jpg' : (100, 100, 150, 150),
    'spongebob.jpg' : (100, 100, 150, 150)
}

#login event
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

#simple Hello! command
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

#getting the user avatar
@bot.command()
async def avatar(ctx, member: discord.Member):
    await ctx.send(member.display_avatar.url)

#code for creating the actual !meme command
@bot.command()
async def meme(ctx, member: discord.Member):
    meme_name = random.choice(list(MEMES.keys()))
    x, y, width, height = MEMES[meme_name]

    meme_path = os.path.join("memes", meme_name)

    avatar_url = member.display_avatar.replace(size=256).url

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            avatar_bytes = await response.read()

    avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
    avatar = avatar.resize((width, height))

    meme = Image.open(meme_path).convert("RGBA")

    meme.paste(avatar, (x, y), avatar)

    output = io.BytesIO()
    meme.save(output, format="PNG")
    output.seek(0)

    await ctx.send(file=discord.File(output, filename="meme.png"))

bot.run(TOKEN)