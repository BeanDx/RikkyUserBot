from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import requests
from pyrogram.types import Message

from bs4 import BeautifulSoup
from pyrogram.types import ChatPermissions
import subprocess
import time
from time import sleep
import random
import random
import asyncio

from pyrogram import Client


app = Client(
    "RikkyUserBot",
    api_id=12345678, # your api_id on https://my.telegram.org/auth
    api_hash="abcdefg" # your api_hash on https://my.telegram.org/auth
)

HELP_COMMAND = '''
<b> RikkyUserBot - это ваш интерактивный многофункциональный помощник в Telegram.\n
Многофункциональный и расширяемый юзербот позволит создавать любые модули, нужна лишь фантазия </b>\n

<em>Наши преимущества:</em> \n
<b> ○ Удобство и простота в использовании </b> \n
<b> ○ Низкая ресурсозатраность </b> \n
<b> ○ Открытый исходный код </b> \n

<a href="https://t.me/PearDe">Создатель</a>
<a href="https://github.com/TreeHack/RikkyUserBot">GitHub проекта</a>
<a href="https://telegra.ph/AKTUALNYJ-SPISOK-KOMAND-RikkyUserBot-11-28">Список команд</a>
<a href="https://t.me/kipt_kate">Дизайнер</a>'''

with app:
    app.send_message("me", "<b>RikkyUserBot запущен успешно ✔</b>\n<b>Введите </b> <code>.help</code> <b>для получения справки </b>")

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)

heartlet_len = joined_heart.count(R)

SLEEP = 0.1


async def _wrap_edit(message: Message, text: str):
    """Floodwait-safe utility wrapper for edit"""
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)


async def phase1(message: Message): # фаза 1
    """Big scroll"""
    BIG_SCROLL = "🧡💛💚💙💜🖤🤎"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


async def phase2(message: Message): # фаза 2
    """Per-heart randomiser"""
    ALL = ["❤️"] + list("🧡💛💚💙💜🤎🖤")  # don't include white heart

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)


async def phase3(message: Message): # фаза 3
    """Fill up heartlet matrix"""
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)


async def phase4(message: Message): # фаза 4
    """Matrix shrinking"""
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)

# ---- Сердечки [.magic] ---- #
@app.on_message(filters.command("magic", prefixes=".") & filters.me) 
async def hearts(_, message: Message):
    await phase1(message)
    await phase2(message)
    await phase3(message)
    await phase4(message)
    await asyncio.sleep(SLEEP * 3)

    final_caption = " ".join(message.command[1:])
    if not final_caption:
        final_caption = ""
    await message.edit(final_caption)

# ---- Скрин сайтов [.site] ---- #
@app.on_message(filters.command("site", prefixes=".") & filters.me)
def screenshot_site(_, msg):
    to_send = msg.text.split(None, 1)
    msg.delete()
    app.send_photo(chat_id=msg.chat.id, photo="https://mini.s-shot.ru/1366x768/JPEG/1366/Z100/?" + to_send[1])



# ---- Команда для тестирования [.test] ---- #
#@app.on_message(filters.command('test', prefixes='.'))
#def test(app, Message):
#    app.send_reaction(Message.chat.id, Message.reply_to_message_id, emoji='🤮')
#    Message.delete()

# ---- Реакции [.react] ---- #
@app.on_message(filters.command('react', prefixes='.'))
def test(app, Message):
    app.send_reaction(Message.chat.id, Message.reply_to_message_id, emoji='🤮') # рыгачка
    Message.delete()

# ---- Команда помощи [.help] ---- #
@app.on_message(filters.command('help', prefixes='.'))
def test(app, message):
    message.delete() # Удаляем сообщение
    app.send_photo(message.chat.id, 'small_ava.jpg', caption=HELP_COMMAND) # отправка фото с локалки


# ---- Команда красивого печатания [.type] ---- #
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
	orig_text = msg.text.split(".type ", maxsplit=1)[1]
	text = orig_text
	tbp = "" # to be printed
	typing_symbol = "|" # ▒

	while(tbp != orig_text):
		try:
			msg.edit(tbp + typing_symbol)
			sleep(0.05) # 50 ms

			tbp = tbp + text[0]
			text = text[1:]

			msg.edit(tbp)
			sleep(0.05)

		except FloodWait as e:
			sleep(e.x)

# ---- Команда взлома пентагона [.hack] ---- #
@app.on_message(filters.command("hack", prefixes=".") & filters.me)
def hack(_, msg):
    perc = 0

    while (perc < 100):
        try:
            text = "👮‍ Взлом пентагона в процессе ..." + str(perc) + "%"
            msg.edit(text)

            perc += random.randint(1, 3)
            sleep(0.1)

        except FloodWait as e:
            sleep(e.x)

    msg.edit("🟢 Пентагон успешно взломан!")
    sleep(3)

    msg.edit("👽 Поиск секретных данных об НЛО ...")
    perc = 0

    while (perc < 100):
        try:
            text = "👽 Поиск секретных данных об НЛО ..." + str(perc) + "%"
            msg.edit(text)

            perc += random.randint(1, 5)
            sleep(0.15)

        except FloodWait as e:
            sleep(e.x)

    msg.edit("🦖 Найдены данные о существовании динозавров на земле!")


# ---- Команда для спама [.spam] ---- #
@app.on_message(filters.command("spam", prefixes=".") & filters.me)
def spam(app, message):
    try:
        spams = " ".join(message.command[2:])
        global number
        number = number + 1
    except:
        message.edit("<b>Вы не ввели число для спама!\nПример:</b><code>.spam 10 текст</code>")
    try:
        for _ in range(int(message.command[1])):
            sleep(0.01)
            app.send_message(message.chat.id, str(spams))
    except IndexError:
        message.edit("<b>Вы не ввели число для спама!\nПример:</b><code>.spam 10 текст</code>")


# ---- Анимация с хлебом [.xleb] ---- #
@app.on_message(filters.command('xleb', prefixes='.') & filters.me)
async def valentine(app, message):
	global number
	await message.edit('⠀👩‍🦰          👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰         👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰        👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰       👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰      👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰     👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰    👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰   👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰  👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰 👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👨‍🦰  ')
	sleep(0.1)
	await message.edit('⠀👩‍🦰💋👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👨‍🦰  ')
	sleep(0.1)
	await message.edit('⠀👩‍🦰  👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👨‍🦰  ')
	sleep(0.1)
	await message.edit('⠀👩‍🦰  👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰  👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👨‍🦰  ')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶 👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶  👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶   👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶    👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶     👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶      👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶       👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶        👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶         👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶')
	sleep(0.2)
	await message.edit('*спустя 5 лет*')
	sleep(3)
	await message.edit('⠀👩‍🦰👶         👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶        👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶       👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶      👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶     👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶    👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶   👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶  👨‍🦰🍞')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞 👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞  👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞   👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞    👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞     👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞      👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞       👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞        👨‍🦰')
	sleep(0.1)
	await message.edit('⠀👩‍🦰👶🍞')

# ---- Анимация с бананом ---- #
banana = '\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️📒📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️📒📒📒📒⬜️ \n⬜️⬜️⬜️⬜️📒📒📒📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️📒📒📒📒⬜️ \n⬜️⬜️⬜️⬜️📒📒📒📒⬜️⬜️ \n⬜️⬛️📒📒📒📒📒⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️📒📒📒📒⬜️ \n⬜️⬜️⬜️⬜️📒📒📒📒⬜️⬜️ \n⬜️⬛️📒📒📒📒📒⬜️⬜️⬜️ \n⬜️⬜️⬜️📒📒📒⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️📒📒📒📒⬜️ \n⬜️⬜️⬜️⬜️📒📒📒📒⬜️⬜️ \n⬜️⬛️📒📒📒📒📒⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️📒📒📒📒⬜️ \n⬜️⬜️⬜️⬜️📒📒📒📒⬜️⬜️ \n⬜️⬛️🟨🟨🟨🟨🟨⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️📒📒📒📒⬜️ \n⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️⬜️ \n⬜️⬛️🟨🟨🟨🟨🟨⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️📒📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️⬜️ \n⬜️⬛️🟨🟨🟨🟨🟨⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️⬜️ \n⬜️⬛️🟨🟨🟨🟨🟨⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒📒⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️⬜️ \n⬜️⬛️🟨🟨🟨🟨🟨⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️📒⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️⬜️ \n⬜️⬛️🟨🟨🟨🟨🟨⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🚪🚪🚪⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🚪⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🟨⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️ \n⬜️⬜️⬜️⬜️🟨🟨🟨🟨⬜️⬜️ \n⬜️⬛️🟨🟨🟨🟨🟨⬜️⬜️⬜️ \n⬜️⬜️⬜️🟨🟨🟨⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️\n\n'
@app.on_message(filters.command('banana', prefixes='.') & filters.me)
async def valentine(app, message):
	global number
	try:
		txt = banana.split('\n\n')
		e = True
		try:
			etime = int(message.text.split('.banana', maxsplit=1)[1])
		except Exception as e:
			try:
				print(f" Ошибка - {e}")
				await message.edit('<b>Вы не ввели число!\nПример:</b> <code>.banana 0</code>')
			finally:
				e = None
				del e

		else:
			for i in txt:
				time = etime
				if e == True:
					e = False
				elif time > 10:
					try:
						await message.edit('<b>Error: Нельзя ставить больше 10с!</b>')
						await asyncio.sleep(0.5)
						await message.delete()
					except:
						pass

				else:
					try:
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
						await message.edit(f"{i}")
						await asyncio.sleep(time)
					except:
						pass

			else:
				number = number + 1
	except Exception as e:
		try:
			print(f"Ошибка - {e}")
		finally:
			e = None
			del e

# ---- Спам гифками [.gifspam] [.gifspam количество] ---- #
@app.on_message(filters.command("gifspam", prefixes=".") & filters.me)
def sendgif(app, message):
	for _ in range(int(message.command[1])):
		sleep(0.01)
		app.send_document(message.chat.id, "https://tenor.com/view/spam-toon-toonio-%D1%82%D1%83%D0%BD%D0%B8%D0%BE-pomidorkin-gif-24712213")

# ---- Анимация со звездочками [.space] ---- #
@app.on_message(filters.command("space", prefixes=".") & filters.me)
async def valentine(app, msg):
	await msg.edit(f'''
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡''')
	sleep(0.5)
	await msg.edit(f'''
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ ''')
	sleep(0.5)
	await msg.edit(f'''
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ ''')
	sleep(0.5)
	await msg.edit(f'''
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ ''')
	sleep(0.5)
	await msg.edit(f'''
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ ''')
	sleep(0.5)
	await msg.edit(f'''
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ ''')
	sleep(0.5)
	await msg.edit(f'''
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * ''')
	sleep(0.5)
	await msg.edit(f'''
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ ''')
	sleep(0.5)
	await msg.edit(f'''
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ 
		☆∴｡　* ''')
	sleep(0.5)
	await msg.edit(f'''
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.
		･ ｡ ''')
	sleep(0.5)
	await msg.edit(f'''
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡
		.''')
	sleep(0.5)
	await msg.edit(f'''
		.
		･ ｡ 
		☆∴｡　* 
		　･ﾟ*｡★･ 
		　　･ *ﾟ｡　　 * 
		　 ･ ﾟ*｡･ﾟ★｡ 
		　　　☆ﾟ･｡°*. ﾟ 
		*　　ﾟ｡·*･｡ ﾟ* 
		　　　ﾟ *.｡☆｡★　･ 
		　　* ☆ ｡･ﾟ*.｡ 
			*　★ ﾟ･｡ * ｡ 
			･　　ﾟ☆ ｡''')
	sleep(5)
	await msg.edit(f'''
		🍃 author: @tgscriptss''')
	sleep(5)
	await msg.delete()
	global number
	number = number + 1

# ---- Поиск мамы [.mum][осуждаю шутки на эту тему!!!] ---- #
@app.on_message(filters.command("mum", prefixes=".") & filters.me)
async def mum(client, message):
	mamka = [f'<b>❌ Мамаша не найдена</b>',f'<b> ✅ МАМАША НАЙДЕНА</b>' ]
	text = "<b>🔍 Поиск твоей мамки начался...</b>"
	await message.edit(str(text))
	await asyncio.sleep(3.0)
	text2 = "<b>🔍 Ищем твою мамашу на Авито... </b>"
	await message.edit(str(text2))
	await asyncio.sleep(1)
	text3 = random.choice(mamka)
	await message.edit(str(text3))
	await asyncio.sleep(3.0)
	text4 = "<b>🔍 Поиск твоей мамаши на свалке... </b>"
	await message.edit(str(text4))
	await asyncio.sleep(3.0)
	text5 = random.choice(mamka)
	await message.edit(str(text5))
	await asyncio.sleep(5.0)

# ---- Анимация бега ---- #
@app.on_message(filters.command("run", prefixes="."))
def run(app, msg):
	testr = 0
	while(testr < 50):
		try:
			text = "🏃"
			msg.edit(text)
			sleep(0.1)
			text = "🚶"
			msg.edit(text)
			sleep(0.1)
			testr += random.randint(1, 3)
		except FloodWait as e:
			sleep(e.x)

	msg.edit("Добежал")

# ---- Визуализацця консоли/терминала ---- #
@app.on_message(filters.command(["console", "cmd"], prefixes="."))
def brain(app, msg):
	msg.edit("`>_`")
	sleep(0.1)
	msg.edit("`>  `")
	sleep(0.1)
	msg.edit("`>_`")
	sleep(0.1)
	msg.edit("`>  `")
	sleep(0.1)
	msg.edit("`>_`")
	sleep(0.1)
	msg.edit("`>c_`")
	sleep(0.1)
	msg.edit("`>cd`")
	sleep(0.1)
	msg.edit("`>cd _`")
	sleep(0.1)
	msg.edit("`>cd p`")
	sleep(0.1)
	msg.edit("`>cd pr_`")
	sleep(0.1)
	msg.edit("`>cd pro`")
	sleep(0.1)
	msg.edit("`>cd proj_`")
	sleep(0.1)
	msg.edit("`>cd proje`")
	sleep(0.1)
	msg.edit("`>cd projec_`")
	sleep(0.1)
	msg.edit("`>cd project`")
	sleep(0.6)
	msg.edit("`>cd project`\n" + "`project>_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>g`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>gi_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git i_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git in`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git ini_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`")
	sleep(0.6)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>g_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>gi`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git a_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git ad`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [=---------] 3%`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [=---------] 5%`")
	sleep(0.3)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [===-------] 30%`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [===-------] 36%`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [====------] 41%`")
	sleep(0.4)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [======----] 67%`")
	sleep(0.2)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>g_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>gi`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git c`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git co_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git com`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git comm_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commi`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -a_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"I`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`")
	sleep(2)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>g_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>gi`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git p`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git pu_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git pus`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push h`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push he_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push her`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push hero_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push herok`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku m`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku ma_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku mas`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku mast_`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku maste`")
	sleep(0.1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku master`")
	sleep(2)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku master`\n" + "`  Counting objects: 100% (5/5), done.`")
	sleep(1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku master`\n" + "`  Counting objects: 100% (5/5), done.\n  Writing objects: 100% (3/3), 364 bytes | 364.00 KiB/s, done.`")
	sleep(1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku master`\n" + "`  Counting objects: 100% (5/5), done.\n  Writing objects: 100% (3/3), 364 bytes | 364.00 KiB/s, done.\n  remote: Compressing source files... done.`")
	sleep(1)
	msg.edit("`>cd project`\n" + "`project>git init`\n" + "`  Git in project/.git/`\n" + "`project>git add .`" + "\n`  [==========] 100%`\n" + "`project>git commit -am \"IT\"`\n" + "`  [master b2a98eb] IT`\n" + "`project>git push heroku master`\n" + "`  Counting objects: 100% (5/5), done.\n  Writing objects: 100% (3/3), 364 bytes | 364.00 KiB/s, done.\n  remote: Compressing source files... done.\n  remote: Verifying deploy... done.`")

	sleep(5)

# ---- Мозг в мусорке [.brain] ---- #
@app.on_message(filters.command(["brain", "b"], prefixes="."))
def brain(app, msg):
	msg.edit("Твой мозг \n🗑          🧠🏃🏻")
	msg.edit("Твой мозг \n🗑         🧠🏃🏻")
	msg.edit("Твой мозг \n🗑        🧠🏃🏻")
	msg.edit("Твой мозг \n🗑       🧠🏃🏻")
	msg.edit("Твой мозг \n🗑      🧠🏃🏻")
	msg.edit("Твой мозг \n🗑     🧠🏃🏻")
	msg.edit("Твой мозг \n🗑    🧠🏃🏻")
	msg.edit("Твой мозг \n🗑   🧠🏃🏻")
	msg.edit("Твой мозг \n🗑 🧠🏃🏻")
	msg.edit("Твой мозг в мусорке \n🗑 🙍🏼‍♂️")

	sleep(5)

# ---- Визуализация вопроса [.quest] ---- #
@app.on_message(filters.command("quest", prefixes=".") & filters.me)
def betaloves(_, msg):
	time = 0.4
	for i in range(1):
		sleep(0.001)
		msg.edit(f'''      
🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦''')  # red
		sleep(0.001)
		msg.edit(f'''      
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''   
🟦🟦🟦🟦🟦🟦🟦
🟦🟦⬛️⬛️⬛️🟦🟦
🟦⬛️🟦🟦🟦⬛️🟦
🟦🟦🟦🟦⬛️🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦⬛️🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦
''')
	sleep(5)

# ---- Обзыватель [.bull] ---- #
@app.on_message(filters.command("bull", prefixes=".") & filters.me)
def valentine(app, message):
	app.send_message(message.chat.id,f'''
<b>помолчи хуета, сиди в обиде ребёнок мертвой шалавы</b>
''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>заебись невъебенным проебом тримандоблядская пиздопроебина воспиздозаолупоклинившаяся в собственном злопиздии.</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>пиздобратия мандопроушечная, уебище залупоглазое</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>дрочепиздище хуеголовое, пробиздоблядская мандопроушина</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>гнидопаскудная хуемандовина</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>ах ты блядь семитаборная чтоб тебя всем столыпином харили</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>охуевшее блядепиздопроёбище чтоб ты хуем поперхнулся долбоебическая пиздорвань</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>хуй тебе в глотку через анальный проход</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>распизди тебя тройным перебором через вторичный переёб пиздоблятское хуепиздрическое мудовафлоебище сосущее километры трипперных членов</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>трихломидозопиздоеблохуе блядеперепиздическая спермоблевотина</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	<b>гандон с гонореей...</b>
	''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>да разъебись ты троебучим проебом сперматоблятская пиздапроебина </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>охуевающая в своей пидарастической сущности похожаю на ебущегося в жопу енота </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>сортирующего яйца в пизде кастрированной кобылы</b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>хуелептический пиздопрозоид, еблоухий мандохвост</b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>ебун хуеголовый, пидрасня ебаная. </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Залупоголовая блядоящерица. .</b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Трипиздоблядская промудохуина! </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Распроеб твою в крестище через коромысло в копейку мать! </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Что за блядская пиздопроебина, охуевающая своей пидорестической заебучестью невъебенной степени охуения. </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Заебись невъебенным проебом тримандоблядская пиздопроебина воспиздозаолупоклинившаяся в собственном злопиздии. </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Мордоблядина залупоглазая.  блядского невъебения! </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Шлюшья мразота приохуебенивающая от собственного недохуеплетского злоетрахания. </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Да произпездуй с 2000 этажа своей припиздоблядской тушей на землю в труху! </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Трипиздоблядское мудопроебное трипиздие, ебоблядище охуевающее от собственной злоебучести.  </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Облямуденный злоебучий страхопизднутый трихуемандаблядский </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>ебаквакнутый распиздаеб... </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Хуесосляблядивый расхуйдяй припиздоблядского четвертоногого происхождения </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>прошу завали свой хуеобрыганский блядозвукоговоритель. </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Промудохуепиздамразоблядское злоепиздие </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>ебоблядищая пиздопроебина сама ахуевающее от того какая оно пездоблядехуепроклятое.</b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Обосробосанная пиздоблядмна двадцати головая семихуюлина припиздовывающее от хуеглотности своей трипиздговноглоталки.</b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Облямудевшая хуеблядина четырестохуйная</b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>вестипёздная мразотоблядская шлюхасосалка. </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>Хуесосная мудохуепиздопроебная мудаблядина сука безмаманя </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>блядь шмара козельуебок сдохни </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>хуесоска  ебланафт чмырь пидорска манда тупая гандопляс пидрила ебалай долбоеб обмудок овцееб дауниха  </b>
	 ''')
	sleep(0.5)
	app.send_message(message.chat.id, f'''
	 <b>ненавижу гомодрилла сучка шлюха трахарила гавносос миньетчик </b>
	 ''')
	sleep(0.5)
	app.send_message(message.chat.id, f'''
	 <b>пидэраст пиздоеб хуеплет кончиглот ебище сын шлюхи гавноеб мудяра </b>
	 ''')
	sleep(0.5)
	app.send_message(message.chat.id, f'''
	 <b>еботрон вафлеглот ебалдуй захуятор имбицил подонок пиздопромудище </b>
	 ''')
	sleep(0.5)
	app.send_message(message.chat.id, f'''
	 <b>выебок ахуяэетер ебозер пиздолиз злоуебок хуиман ебил долбоебина пиндос мудазвон </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>хуеб амеба хуйло хуила пиздорвань смесь ебланства и говна ебанат </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>умалишенный дегенерат мандопроушина очкоблут порванный обрубок хуяраспиздяй свинозалупа</b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>семиголовый восьмихуй ебоблядище свинохуярище вафлепиздище хуй лохматый жопа рванная мудопроеб </b>
	 ''')
	sleep(1)
	app.send_message(message.chat.id, f'''
	 <b>страхапиздище ебосос дурфанка косоуебище долбоногий лихохуетень</b>
	 ''')
	sleep(1)

# ---- Диз из бравл старса [.dis] ---- #
@app.on_message(filters.command("dis", prefixes=".") & filters.me)
def betaloves(_, msg):
	time = 0.6
	for i in range(1):
		msg.edit(f'''
🟥''')  # red
		sleep(0.001)
		msg.edit(f'''
🟥🟥''')  # red
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥🟥🟥🟥🟥🟥''')
		sleep(0.001)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥🟥🟥🟥🟥🟥🟥''')
		sleep(1)
		msg.edit(f'''
🈲🈲🈲🈲🈲🈲🈲🈲
🈲🈲⬜️⬜️⬜️🈲⬜️🈲
🈲🈲⬜️⬜️⬜️🈲⬜️🈲
🈲⬜️⬜️⬜️⬜️🈲⬜️🈲
🈲🈲🈲🈲⬜️🈲🈲🈲
🈲🈲🈲🈲🈲🈲🈲🈲''')
		sleep(1)
		msg.edit(f'''
🟥🟥🟥🟥🟥🟥🟥🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥🟥⬜️⬜️⬜️🟥⬜️🟥
🟥⬜️⬜️⬜️⬜️🟥⬜️🟥
🟥🟥🟥🟥⬜️🟥🟥🟥
🟥🟥🟥🟥🟥🟥🟥🟥
''')
		sleep(1)
		msg.edit(f'''
🈲🈲🈲🈲🈲🈲🈲🈲
🈲🈲⬜️⬜️⬜️🈲⬜️🈲
🈲🈲⬜️⬜️⬜️🈲⬜️🈲
🈲⬜️⬜️⬜️⬜️🈲⬜️🈲
🈲🈲🈲🈲⬜️🈲🈲🈲
🈲🈲🈲🈲🈲🈲🈲🈲''')
		sleep(4)


# ---- Лайк из бравл старса [.like] ---- #
@app.on_message(filters.command("like", prefixes=".") & filters.me)
def betaloves(_, msg):
	time = 0.6
	for i in range(1):
		msg.edit(f'''      
🟦''')  # red
		sleep(0.001)
		msg.edit(f'''
🟦🟦''')  # red
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦🟦🟦🟦🟦🟦''')
		sleep(0.001)
		msg.edit(f'''
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦⬜️🟦🟦🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦⬜️⬜️⬜️🟦⬜️🟦
🟦🟦🟦🟦🟦🟦🟦🟦''')
		sleep(5)

# ---- Оксимирон [.versus] [.Oxxxymiron] [.battle] ---- #
@app.on_message(filters.command(["Oxxxymiron", "versus", "battle"], prefixes=".") & filters.me)
def valentine(app, msg):
	app.send_message(msg.chat.id, f'''
	<b>Гавно</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Залупа</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Пенис</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Хер</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Давалка</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Хуй</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Блядина</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Галовка</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Шлюха</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Жопа</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Член</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Еблан</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Петух</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Мудила</b>
	''')
	sleep(0.7)
	app.send_message(msg.chat.id, f'''
	<b>Рукаблуд</b>
	''')
	sleep(0.5)
	app.send_message(msg.chat.id, f'''
	<b>Ссанина</b>
	''')
	sleep(0.5)
	app.send_message(msg.chat.id, f'''
	<b>Очко</b>
	''')
	sleep(0.5)
	app.send_message(msg.chat.id, f'''
	<b>Блядун</b>
	''')
	sleep(0.5)
	app.send_message(msg.chat.id, f'''
	<b>Вагина</b>
	''')
	sleep(0.4)
	app.send_message(msg.chat.id, f'''
	<b>Сука</b>
	''')
	sleep(0.4)
	app.send_message(msg.chat.id, f'''
	<b>Ебланище</b>
	''')
	sleep(0.4)
	app.send_message(msg.chat.id, f'''
	<b>Влагалеще</b>
	''')
	sleep(0.4)
	app.send_message(msg.chat.id, f'''
	<b>Пердун</b>
	''')
	sleep(0.4)
	app.send_message(msg.chat.id, f'''
	<b>Дрочила</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Пидор</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Пизда</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Туз</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Малафья</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Гомик</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Мудила</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Пилотка</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Манда</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Анус</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Вагина</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Путана</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Педрила</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Шалава</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Хуила</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Мошонка</b>
	''')
	sleep(0.3)
	app.send_message(msg.chat.id, f'''
	<b>Елда</b>
	''')
	sleep(0.8)
	app.send_message(msg.chat.id, f'''
	<b>Раунд!</b>
	''')

	sleep(5)

# ---- Превращение в гея [.gay] ---- #
@app.on_message(filters.command("gay", prefixes=".") & filters.me)
def betaloves(_, msg):
	gay1 = 0

	msg.edit(f'''
	Превращяем тебя в гея!''')
	sleep(0.6)
	while gay1 <= 100:
		sleep(0.1)
		gay1 += 1
		msg.edit(f'''
		{gay1}%''')
	if gay1 >= 100:
		msg.edit(f'''
		Загрузка.''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка..''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка...''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка.''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка..''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка...''')
		sleep(0.6)
		msg.edit(f'''
		Смена ориентации.''')
		sleep(0.6)
		msg.edit(f'''
		Смена ориентации..''')
		sleep(0.6)
		msg.edit(f'''
		Смена ориентации...''')
		sleep(0.6)
		msg.edit(f'''
		Смена ориентации.''')
		sleep(0.6)
		msg.edit(f'''
		Смена ориентации..''')
		sleep(0.6)
		msg.edit(f'''
		Смена ориентации...''')
		sleep(0.6)
		msg.edit(f'''
		Подождите немного.''')
		sleep(0.6)
		msg.edit(f'''
		Подождите немного..''')
		sleep(0.6)
		msg.edit(f'''
		Подождите немного...''')
		sleep(0.6)
		msg.edit(f'''
		Подождите немного.''')
		sleep(0.6)
		msg.edit(f'''
		Подождите немного..''')
		sleep(0.6)
		msg.edit(f'''
		Подождите немного...''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка почти завершена.''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка почти завершена..''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка почти завершена...''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка почти завершена.''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка почти завершена..''')
		sleep(0.6)
		msg.edit(f'''
		Загрузка почти завершена...''')
		sleep(1)
		msg.edit(f'''
		Поздравляем! Загрузка успешно завершена! ''')
		sleep(1)
		msg.edit(f'''
		Теперь ты 100% гей! ''')

	sleep(5)

# ---- оскорбление админа [.adm] ---- #
@app.on_message(filters.command("adm", prefixes=".") & filters.me)
def betaloves(_, msg):
	onal = 0
	onal2 = random.randint(0, 325)

	msg.edit(f'''
	Поиск админа.''')
	sleep(0.6)
	msg.edit(f'''
	Поиск админа..''')
	sleep(0.6)
	msg.edit(f'''
	Поиск админа...''')
	sleep(0.6)
	msg.edit(f'''
	Админ найден!''')
	sleep(0.8)
	msg.edit(f'''
	Идёт поиск анального отверстия админа.''')
	sleep(0.6)
	msg.edit(f'''
	Идёт поиск анального отверстия админа..''')
	sleep(0.6)
	msg.edit(f'''
	Идёт поиск анального отверстия админа...''')
	sleep(0.6)
	msg.edit(f'''
	Найдено!''')
	sleep(0.8)
	msg.edit(f'''
	Измерение анального отверстия админа.''')
	sleep(0.6)
	msg.edit(f'''
	Измерение анального отверстия админа..''')
	sleep(0.6)
	msg.edit(f'''
	Измерение анального отверстия админа...''')
	sleep(0.6)
	msg.edit(f'''
	Анальное отверстие админа состовляет {onal2} км''')
	sleep(1)
	while onal <= 55:
		sleep(0.1)
		onal += 1
		msg.edit(f'''
		Анальное проникновение админу выполнено на {onal}%''')
	if onal == 56:
		sleep(0.3)
		onal += 1
		msg.edit(f'''
		Рука устала''')
		sleep(0.6)
		msg.edit(f'''
		Отдых руки.''')
		sleep(0.6)
		msg.edit(f'''
		Отдых руки..''')
		sleep(0.6)
		msg.edit(f'''
		Отдых руки...''')
		sleep(0.6)
		msg.edit(f'''
		Отдых руки.''')
		sleep(0.6)
		msg.edit(f'''
		Отдых руки..''')
		sleep(0.6)
		msg.edit(f'''
		Отдых руки...''')
		sleep(0.6)
		msg.edit(f'''
		Рука отдохнула, можно продолжать...''')
		sleep(0.8)
		while onal >= 57:
			sleep(0.1)
			onal += 1
			msg.edit(f'''
			Анальное проникновение админу выполнено на {onal}%''')
			if onal == 99:
				sleep(0.6)
				msg.edit(f'''
				Жопа админа порвана. Поздравляю!''')
				break

	sleep(5)

# ---- Рандом выбор да/нет [.try] ---- #
@app.on_message(filters.command("try", prefixes=".") & filters.me)
def betaloves(_, msg):
	t = ["[Да]", "[Нет]"]

	try0 = random.choice(t)
	try1 = " ".join(msg.command[1:])

	if not try1:
		msg.edit(f'''
			**Error: Вы не ввели вопрос!\nИспользование: .try <вопрос>**''')
		sleep(3)
		msg.delete()
	else:
		msg.edit(f'''
			{try1} {try0}''')

	sleep(5)

# ---- Анимация текста [.text] ---- #
@app.on_message(filters.command("text", prefixes=".") & filters.me)
def betaloves(_, msg):
	text1 = " ".join(msg.command[1:])

	if not text1:
		msg.edit(f'''
			**Error: Вы не ввели текст!\nИспользование: .text <текст>**''')
		sleep(1.5)
		msg.delete()
	else:
		msg.edit(f'''
			{text1}ㅤㅤㅤㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤ{text1}ㅤㅤㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤㅤ{text1}ㅤㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤㅤㅤ{text1}ㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤㅤㅤㅤ{text1}ㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤㅤㅤㅤㅤ{text1}''')
		sleep(0.5)
		msg.edit(f'''
			ㅤㅤㅤㅤ{text1}ㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤㅤㅤ{text1}ㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤㅤ{text1}ㅤㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			ㅤ{text1}ㅤㅤㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			{text1}ㅤㅤㅤㅤㅤ''')
		sleep(0.5)
		msg.edit(f'''
			{text1}''')

	sleep(5)

# ---- Команда для Кати [.Kate] ---- #
@app.on_message(filters.command("Kate", prefixes=".") & filters.me)
async def valentine(app, msg):
    time.sleep(.25)
    await msg.edit('🖼')
    time.sleep(.25)           # 🖼
    await msg.edit('🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 ')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')

    time.sleep(.25)
    await msg.edit('🎨 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🖼 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🖼 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🖼\n🖼 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🖼 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🖼 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🖼 🎨\n🎨 🎨 🎨 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🖼\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🖼 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🖼 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🖼 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🖼 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🖼')
    time.sleep(.25)
    await msg.edit('🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨')

    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨')
    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 💛\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨')
    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 💛\n💛 🎨 🎨 🎨\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨')
    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n🎨 🎨 🎨 🎨\n🎨 🎨 🎨 🎨')
    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n💛 🎨 🎨 🎨\n🎨 🎨 🎨 🎨')
    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n🎨 🎨 🎨 🎨')
    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n💛 🎨 🎨 🎨')
    time.sleep(.25)
    await msg.edit('💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n💛 🎨 🎨 💛\n💛 🎨 🎨 💛')
    time.sleep(.25)
    await msg.edit('💛 💛 🎨 💛\n💛 💛 🎨 💛\n💛 💛 🎨 💛\n💛 💛 🎨 💛')
    time.sleep(.25)
    await msg.edit('💛        <b>Для</b>      💛\n❤️       <b>Кати</b>     ❤️\n💛        ❤️        💛\n💛 <a href="https://t.me/kipt_kate">Дизайнер</a> 💛', disable_web_page_preview=True)
    
    # 💛 желтое


app.run()