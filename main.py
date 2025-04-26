import telebot
import os
from logic import mineral_detect

# Инициализация бота
bot = telebot.TeleBot("")

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я твой телеграм бот. Напиши /help, чтобы увидеть список команд"
    )

@bot.message_handler(content_types=["photo"])
def est_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, "Вы не отправили фотографию")
    
    try:
        # Получаем информацию о файле
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Создаем папку images, если ее нет
        if not os.path.exists('images'):
            os.makedirs('images')
            
        # Сохраняем файл
        file_name = f"images/{file_info.file_id}.jpg"
        with open(file_name, "wb") as new_file:
            new_file.write(downloaded_file)
        
        # Анализируем изображение
        result = mineral_detect(file_name)
        bot.reply_to(message, f"Результат анализа: {result}")
        
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

# Запуск бота
bot.polling()
