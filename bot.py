import telebot
from telebot import types
import json
from datetime import datetime
import re

TOKEN = "8074790862:AAFGTqIB2asQQpsN-12ev38zs5Za0JcLccE"
ADMIN_IDS = [587530809, 5396284860]

bot = telebot.TeleBot(TOKEN)

bot.set_my_commands([
    types.BotCommand("/start", "Botni ishga tushirish"),
    types.BotCommand("/help", "🔴 AFU profilaktika inspektori 🔴"),
    types.BotCommand("/afu_murojaat", "🔴 SOS 🔴"),
])

FILTER_WORDS = [
    'pichoq', 'lim','urish','уриш','паросат','parosat', 'haqorat', 'janjal', 'sex', 'irqiy', 'siyosiy', 'nashida',
    'din', 'kamsitish', 'boron', 'qattiq', 'hasad', 'qotil', 'psix', 'zo‘ravon',
    'terror', 'qatl', 'shahvat', 'nafrat', 'zarar','qo‘pol', 'noqonuniy', 'qochqin', 'uchrashuv', 'shilqim', 'shovqin',
    'pornografiya', 'adovat', 'fohisha', 'iflos', 'qallob', 'shayton','пичоқ', 'лим', 'ҳақорат', 'жанджал', 'секс', 'ирқий', 'сиёсий', 'нашидa',
    'дин', 'камситиш', 'ифлос', 'отил', 'ҳасад', 'қотиллик', 'псих', 'зўравонлик',
    'талқин', 'террор', 'қатл', 'шаҳват', 'нафрат', 'зарар', 'қўпол', 'яроқ', 'ноқонуний', 'қочқин', 'тўқнашув', 'тежовсиз', 'шовқин',
    'порнография', 'адоват', 'фоҳиша', 'сўкки', 'қаллоблик', 'майҳар', 'шайтон',
]

try:
    with open("user_data.json", "r", encoding="utf-8") as f:
        user_data = json.load(f)
except:
    user_data = {}

def save_user_data():
    with open("user_data.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

def log_event(entry):
    try:
        with open("log.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []
    data.append(entry)
    with open("log.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@bot.message_handler(commands=['start'])
def start_command(message):
    text = (
        "👋 Salom! Bu bot orqali siz AFU profilaktika inspektoriga murojaat yuborishingiz mumkin @AFUqalqonbot ga o'ting .\n\n"
        "👇 Quyidagi tugmani bosing:"
    )
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🚘 AFU inspektoriga murojaat", callback_data="afu_murojaat")
    markup.add(btn)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "afu_murojaat")
def handle_afu_button(call):
    text = (
        "📲 Iltimos, telefon raqamingizni yuboring.\n"
        "So‘ng murojaatingizni quyidagi formatda yozing:\n\n"
        "<b>Ism Familiya:</b> [Ismingiz]\n"
        "<b>Telefon raqami:</b> [Raqamingiz]\n"
        "<b>Murojaat matni:</b> [Muammo yoki xabaringizni yozing]\n\n"
        "🔐 Ma’lumotlaringiz maxfiy saqlanadi."
    )
    request_contact_btn = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    request_contact_btn.add(types.KeyboardButton("📞 Raqamni yuborish", request_contact=True))
    bot.send_message(call.message.chat.id, text, reply_markup=request_contact_btn, parse_mode="HTML")

@bot.message_handler(commands=['afu_murojaat'])
def afu_murojaat_command(message):
    text = (
        "📲 Iltimos, quyidagi botga o‘ting va telefon raqamingizni yuboring.\n"
        "So‘ng murojaatingizni quyidagi formatda yuboring:\n\n"
        "<b>Ism Familiya:</b> [Ismingiz]\n"
        "<b>Telefon raqami:</b> [Raqamingiz]\n"
        "<b>Murojaat matni:</b> [Muammo yoki xabaringizni yozing]\n\n"
        "🔐 Ma’lumotlaringiz faqat maxfiy tarzda inspektorga yetkaziladi."
    )
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🛡 AFU Qalqon botga o‘tish", url="https://t.me/AFUqalqonbot")
    markup.add(btn)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
        "🟤Ibragimov Qahramon Abduhamitxon o‘g‘li - Alfraganus universiteti munitsipal profilaktika katta inspektori, kapitan.\n\n"
        "🔵 UNIVERSITET HUDUDIDAGI HUQUQBUZARLIK HOLATIDA USHBU RAQAMGA QO‘NG‘IROQ QILING: (99) 998-47-02"
    )

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    user_data[str(message.from_user.id)] = {
        "phone": message.contact.phone_number,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name
    }
    save_user_data()
    bot.send_message(message.chat.id, "✅ Raqamingiz saqlandi. Endi murojaatingizni yozing.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = str(message.from_user.id)
    text = message.text or ""
    lower_text = text.lower()
    username = message.from_user.username or "no_username"
    first_name = message.from_user.first_name
    chat_id = message.chat.id
    phone = user_data.get(user_id, {}).get("phone", "nomaʼlum")
    group_name = message.chat.title if message.chat.type in ['group', 'supergroup'] else "Shaxsiy"
    group_link = f"https://t.me/c/{str(chat_id)[4:]}" if message.chat.type in ['group', 'supergroup'] else "Shaxsiy"

    for word in FILTER_WORDS:
        if re.search(fr"{word}", lower_text):
            event = {
                "type": "filter",
                "chat_id": chat_id,
                "group_name": group_name,
                "group_link": group_link,
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "phone": phone,
                "message": text,
                "word": word,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            log_event(event)
            warning = (
                f"⚠️ <b>Filtrlangan so‘z aniqlandi</b>\n\n"
                f"👤 Ismi: {first_name}\n"
                f"🔗 Username: @{username}\n"
                f"🆔 ID: <code>{user_id}</code>\n"
                f"📞 Telefon: {phone}\n"
                f"💬 Xabar: {text}\n"
                f"🚫 So‘z: <b>{word}</b>\n"
                f"👥 Guruh: {group_name}\n"
                f"🔗 Havola: {group_link}"
            )
            for admin_id in ADMIN_IDS:
                bot.send_message(admin_id, warning, parse_mode="HTML")
            return

    if message.chat.type == "private":
        event = {
            "type": "sos",
            "chat_id": chat_id,
            "group_name": group_name,
            "group_link": group_link,
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "phone": phone,
            "message": text,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        log_event(event)
        sos_text = (
            f"📥 <b>Yangi murojaat</b>\n\n"
            f"👤 Ismi: {first_name}\n"
            f"🔗 Username: @{username}\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"📞 Telefon: {phone}\n"
            f"💬 Murojaat: {text}"
        )
        for admin_id in ADMIN_IDS:
            bot.send_message(admin_id, sos_text, parse_mode="HTML")

bot.polling(none_stop=True)
