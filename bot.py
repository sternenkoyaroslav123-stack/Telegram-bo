import telebot
from telebot import types

# === ТВОИ ДАННЫЕ ===
TOKEN = "8029627101:AAFl0AUzVgpPmImWzAoc6FaAPibGxNsiRJI"
ADMIN_ID = 8295534561
CHANNEL_ID = -1002361562441

bot = telebot.TeleBot(TOKEN)

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Отправь мне сообщение — я передам его админу на анонимную публикацию."
    )

# === Обработка сообщений пользователей ===
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'voice'])
def handle_message(message):
    try:
        # Сообщение пользователю
        bot.send_message(
            message.chat.id,
            "✅ Сообщение отправлено админу на обработку анонимно."
        )

        # Формируем ссылку на пользователя
        if message.from_user.username:
            username_link = f"@{message.from_user.username}"
        else:
            username_link = f"[Пользователь без username](tg://user?id={message.from_user.id})"

        # === Формируем сообщение админу ===
        # Отправляем само сообщение (текст/медиа)
        if message.content_type == "text":
            sent = bot.send_message(
                ADMIN_ID,
                f"💌 Новое сообщение:\n\n🗨 {message.text}"
            )
        elif message.content_type == "photo":
            file_id = message.photo[-1].file_id
            caption = message.caption if message.caption else "📷 Фото без подписи"
            sent = bot.send_photo(ADMIN_ID, file_id, caption=f"💌 Новое сообщение:\n\n🗨 {caption}")
        elif message.content_type == "video":
            file_id = message.video.file_id
            caption = message.caption if message.caption else "🎥 Видео без подписи"
            sent = bot.send_video(ADMIN_ID, file_id, caption=f"💌 Новое сообщение:\n\n🗨 {caption}")
        elif message.content_type == "document":
            file_id = message.document.file_id
            caption = message.caption if message.caption else "📄 Документ"
            sent = bot.send_document(ADMIN_ID, file_id, caption=f"💌 Новое сообщение:\n\n🗨 {caption}")
        elif message.content_type == "voice":
            file_id = message.voice.file_id
            sent = bot.send_voice(ADMIN_ID, file_id, caption="🎤 Голосовое сообщение")
        else:
            sent = bot.send_message(ADMIN_ID, "⚠️ Неизвестный тип сообщения.")

        # Добавляем кнопку "Опубликовать"
        markup = types.InlineKeyboardMarkup()
        publish_btn = types.InlineKeyboardButton(
            text="📢 Опубликовать в канал",
            callback_data=f"publish_{message.chat.id}_{message.message_id}"
        )
        markup.add(publish_btn)
        bot.edit_message_reply_markup(ADMIN_ID, sent.message_id, reply_markup=markup)

        # Отправляем второе сообщение — от кого
        bot.send_message(
            ADMIN_ID,
            f"🔗 От кого: {username_link}",
            parse_mode='Markdown'
        )

    except Exception as e:
        print(f"[ОШИБКА при обработке сообщения] {e}")

# === Обработка нажатия кнопки публикации ===
@bot.callback_query_handler(func=lambda call: call.data.startswith("publish_"))
def publish_to_channel(call):
    try:
        parts = call.data.split("_")
        user_id = int(parts[1])
        msg_id = int(parts[2])

        bot.copy_message(CHANNEL_ID, user_id, msg_id)
        bot.answer_callback_query(call.id, "✅ Сообщение опубликовано в канал!")

    except Exception as e:
        print(f"[ОШИБКА публикации] {e}")
        bot.answer_callback_query(call.id, "⚠️ Ошибка при публикации!")

# === Запуск ===
print("🤖 Бот запущен и работает...")
bot.infinity_polling()
