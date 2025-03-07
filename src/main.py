import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("EDITOR_CHANNEL_ID")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

global input_mode
global code

input_mode = 0  # 0:コマンド入力モード, 1:メッセージ入力モード
line_symbol = "========================================================"
code = []


@bot.event
async def on_ready():
    input_mode = 0
    code = []
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Sync error: {e}")


async def all_messages_delete(channel_ID=CHANNEL_ID):
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


async def show_editor(message, code, stack_trace="#"):
    await all_messages_delete()
    await message.channel.send(line_symbol)
    for i, line in enumerate(code):
        await message.channel.send(f"{i} | {line}")
    await message.channel.send(line_symbol)
    await show_terminal(message, stack_trace)


async def show_terminal(message, stack_trace: str):
    await message.channel.send(f"```\nterminal\n|\n{stack_trace}\n```")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        if message.content=="new":
            await show_editor(message, [], "all deleted")
            return
        # 入力モード切り替え
        code = [
            "import discord",
            "from discord.ext import commands",
            "import os",
            "from dotenv import load_dotenv",
            "load_dotenv()",
            "TOKEN = os.getenv",
        ]
        if input_mode == 0:
            # コマンド入力モード
            await show_editor(message, code, "mode: command input")
            pass
        else:
            # メッセージ入力モード
            await show_editor(message, code, "mode: message input")
            pass
        # print("on_message")
        # tmp_message = message.content
        # await message.channel.send(tmp_message)
        # await message.delete()
    except discord.Forbidden:
        await message.channel.send("❌ メッセージ削除権限がありません！")
    except discord.HTTPException as e:
        await message.channel.send(f"❌ エラーが発生しました: {e}")


bot.run(TOKEN)
