import telebot
from telebot import types

# === НАСТРОЙКИ ===
TOKEN = "8029627101:AAFl0AUzVgpPmImWzAoc6FaAPibGxNsiRJI"
ADMIN_ID = 8295534561
CHANNEL_ID = -1002361562441

bot = telebot.TeleBot(TOKEN)

# === СТАРТ ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Отправь мне сообщение — я передам его админу для анонимной публикации.")

# === ПОЛУЧЕНИЕ СООБЩЕНИЙ ===
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'voice'])
def handle_message(message):
    try:
        bot.send_message(message.chat.id, "✅ Сообщение отправлено админу на обработку анонимно.")

        if message.from_user.username:
            username_link = f"@{message.from_user.username}"
        else:
            username_link = f"[Пользователь без username](tg://user?id={message.from_user.id})"

        # Отправляем админу сообщение
        if message.text:
            bot.send_message(ADMIN_ID, f"💌 Новое сообщение:\n\n🗨 {message.text}", parse_mode='Markdown')
        else:
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

        # Кнопка "Опубликовать в канал"
        markup = types.InlineKeyboardMarkup()
        publish_btn = types.InlineKeyboardButton(
            text="📢 Опубликовать в канал",
            callback_data=f"publish_{message.chat.id}_{message.message_id}"
        )
        markup.add(publish_btn)

        # Отправляем ссылку на пользователя отдельным сообщением
        bot.send_message(ADMIN_ID, f"🔗 От кого: {username_link}", parse_mode='Markdown', reply_markup=markup)

    except Exception as e:
        print(f"[ОШИБКА] {e}")

# === ПУБЛИКАЦИЯ В КАНАЛ ===
@bot.callback_query_handler(func=lambda call: call.data.startswith("publish_"))
def publish_to_channel(call):
    try:
        _, user_id, msg_id = call.data.split("_")
        bot.copy_message(CHANNEL_ID, int(user_id), int(msg_id))
        bot.answer_callback_query(call.id, "✅ Сообщение опубликовано в канал!")
    except Exception as e:
        bot.answer_callback_query(call.id, f"⚠️ Ошибка: {e}")

print("🤖 Бот запущен и работает...")
bot.infinity_polling()
