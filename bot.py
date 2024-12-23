import sqlite3

from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import sys


app = Flask(__name__)

# Инициализация бота
updater = Updater(token='7919466486:AAEy0pyH1Dtcy5fkGBXhsH5GlSpUXlzgBW8', use_context=True)
dispatcher = updater.dispatcher


# Команда /start с кнопкой для открытия сайта как Web App
def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение и меню с кнопкой для открытия веб-сайта как Web App"""
    # Создаем кнопку с открытием веб-приложения

    web_app_url = f"https://041b-146-70-85-138.ngrok-free.app/"


    keyboard = [
        [InlineKeyboardButton("Открыть веб-приложение", web_app=WebAppInfo(url=web_app_url))],
        # [InlineKeyboardButton("Проверить подлючение к рассылке", callback_data='other_command')]
    ]

    # Отправляем сообщение с прикрепленной клавиатурой
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "приветственное сообщение",
        reply_markup=reply_markup
    )


# Обработка нажатия на кнопки
def button(update: Update, context: CallbackContext) -> None:
    """Обрабатывает нажатие кнопок в InlineKeyboard"""
    query = update.callback_query
    query.answer()  # Обязательно подтверждаем обработку нажатия

    if query.data == 'other_command':
        query.edit_message_text(text="Вы выбрали другую команду.")
        print('sddsf')

# Обработка текста
def echo(update: Update, context: CallbackContext) -> None:
    """Эхо-функция для обработки обычных текстовых сообщений"""
    update.message.reply_text(f"Вы написали: {update.message.text}")


# Маршрут для отправки сообщения через Flask
@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.json
    chat_id = content['chat_id']
    message = content['message']
    updater.bot.send_message(chat_id=chat_id, text=message)

    return jsonify({'status': 'ok'})


# Основная функция
def main():
    # Добавляем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))  # Команда для вызова меню
    dispatcher.add_handler(CallbackQueryHandler(button))  # Обработчик для нажатий кнопок
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))  # Обработчик для текстовых сообщений

    # Запуск бота
    updater.start_polling()

    # Запуск Flask сервера
    app.run(host='0.0.0.0', port=5000)


# Запуск программы
if __name__ == '__main__':
    main()
