import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from word_db import WordDB

load_dotenv()
db = WordDB("word_db.txt")

'''
주요 객체들.
Client, Intent, Message, Embed, Interaction, View, UI Component,

'''

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

user_states: dict[int, str] = {}

@tree.command(name="ping", description="ping test")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Bot online")

@tree.command(name="jquiz", description="japanese quiz start")
async def jquiz(interaction: discord.Interaction):
    quiz = db.get_one_random()
    word: str = quiz[1]
    answer: str = quiz[0]
    await interaction.response.send_message(f" # {word} - ||{answer}||")

@tree.command(name="start_demo", description="yes/no 분기 데모")
async def start_demo(interaction: discord.Interaction):
    user_id = interaction.user.id
    print(user_id)

    # 이 유저의 "다음 한 번의 답장"을 기다리겠다는 상태 저장
    user_states[user_id] = "waiting_yes_no_answer"

    # 첫 응답은 반드시 interaction.response 로
    await interaction.response.send_message(
        "안녕하세요! 이제 채팅창에 `yes` 또는 `no` 를 입력해 보세요.\n"
        "당신의 답에 따라 다른 로직이 실행됩니다 🙂"
    )

@client.event
async def on_message(message: discord.Message):
    # 봇 자기 자신이나 다른 봇은 무시
    if message.author.bot:
        return

    user_id = message.author.id
    print(user_id)
    state = user_states.get(user_id)
    print(user_id)

    # 현재 이 유저의 답장을 기다리는 상태인지 확인
    if state == "waiting_yes_no_answer":
        content = message.content.strip().lower()

        if content == "yes":
            # YES 로직
            await message.channel.send(
                "✅ YES 를 선택하셨네요! 여기서 YES용 로직을 실행하면 됩니다."
            )

        elif content == "no":
            # NO 로직
            await message.channel.send(
                "❌ NO 를 선택하셨네요! 여기서 NO용 로직을 실행하면 됩니다."
            )

        else:
            # 의도한 답변이 아닌 경우
            await message.channel.send(
                "죄송해요, 이해하지 못했어요. `yes` 또는 `no` 중 하나로 답해주세요!"
            )
            # 상태를 유지해서 다시 입력 받을 수 있게 함
            return

        # 한 번 처리했으면 상태 초기화 (원샷 입력)
        user_states.pop(user_id, None)

# --- on_ready: 슬래시 명령어 등록(sync) ---
@client.event
async def on_ready():
    # 전역 sync (모든 guild)
    await tree.sync()
    print(f"Bot ready as {client.user} (ID: {client.user.id})")


# --- Run ---
client.run(os.getenv("BOT_TOKEN"))
