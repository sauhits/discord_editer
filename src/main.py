import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
line_counter = 0
stack_trace = "#"
input_mode = 0  # 0:コマンド入力モード, 1:メッセージ入力モード


@bot.event
async def on_ready():
    global line_counter
    line_counter = 0
    global stack_trace
    stack_trace = "#"
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")

    except Exception as e:
        print(f"Sync error: {e}")


async def all_messages_delete(channel_ID):
    try:
        channel = await bot.fetch_channel(channel_ID)
        messages = []
        async for message in channel.history(limit=100):
            messages.append(message)
        if messages:
            for message in messages:
                await message.delete()

    except Exception as e:
        print(f"Error deleting messages: {e}")


@bot.tree.command(name="edit", description="Edit a message")
async def edit(interaction: discord.Interaction):
    global line_counter
    global stack_trace
    stack_trace = "#"
    line_counter = 0
    line_symbol = "=================================================================================================================="
    await all_messages_delete(1347111148335665213)
    await interaction.response.send_message(
        f"|\n{line_symbol}\n{line_counter} | \n{line_symbol}\n```\nterminal\n|\n{stack_trace}\n```"
    )


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        print("on_message")
        tmp_message = message.content
        await message.channel.send(tmp_message)
        await message.delete()
    except discord.Forbidden:
        await message.channel.send("❌ メッセージ削除権限がありません！")
    except discord.HTTPException as e:
        await message.channel.send(f"❌ エラーが発生しました: {e}")


bot.run(TOKEN)
