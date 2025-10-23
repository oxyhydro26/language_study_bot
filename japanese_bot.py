import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from word_db import WordDB

load_dotenv()
db = WordDB("word_db.txt")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="ping", description="ping test")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Bot online")

@tree.command(name="jquiz", description="japanese quiz start")
async def ping(interaction: discord.Interaction):
    quiz = db.get_one_random()
    word: str = quiz[1]
    answer: str = quiz[0]
    await interaction.response.send_message(f" # {word} - ||{answer}||")

@client.event
async def on_ready():
    await tree.sync()
    print("Bot ready")

client.run(os.getenv('BOT_TOKEN'))
