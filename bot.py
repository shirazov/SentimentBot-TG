import telebot
from telebot import types
import sys
import time
import threading
import os
from pars import fetch_comments, save_to_excel  # Импортируем функции из pars.py

import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
import joblib

tokenizer = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment')
# Загрузка модели
model = AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment', return_dict=True)
#model = joblib.load('model.pkl')
# Загрузка векторизатора
vectorizer = joblib.load('vectorizer.pkl')

# Токен API
API_TOKEN = '7912201524:AAEQ36m7T9FU5cGqR3Jb2zSDofa8jM5DwgM'

# Создание бота
bot = telebot.TeleBot(API_TOKEN)

# Функция для анализа тональности комментария
@torch.no_grad()
def analyze_sentiment(comment):
    inputs = tokenizer(comment, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()
# @torch.no_grad()
# def analyze_sentiment(comment):
#     # Преобразуем комментарий в вектор
#     comment_vect = vectorizer.transform([comment])
#     predicted = model.predict(comment_vect)

    # Оценка на основе полярности
    if predicted[0] == 1:
        return "Позитивный"
    elif predicted[0] == 2:
        return "Негативный"
    else:
        return "Нейтральный"

# Оценка на основе полярности
    # if predicted[0] == 'positive':
    #     return "Позитивный"
    # elif predicted[0] == 'negative':
    #     return "Негативный"
    # else:
    #     return "Нейтральный"


# Клавиатура для выбора режима
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button1 = types.KeyboardButton("1")
button2 = types.KeyboardButton("2")
keyboard.add(button1, button2)

# Хендлер для команды /start
@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привет! Выберите режим:\n1. Один комментарий (просмотр логики работы ИИ)\n2. Суммаризатор отзывов (выжмит самый сок из массы отзывов)",
        reply_markup=keyboard
    )

# Хендлер для выбора режима 1
@bot.message_handler(func=lambda message: message.text == "1")
def mode_1(message):
    bot.send_message(message.chat.id, "Вы выбрали Режим 1. Отправьте комментарий для анализа.")
    bot.register_next_step_handler(message, handle_single_comment)

# Хендлер для обработки комментария в Режиме 1
def handle_single_comment(message):
    # Анализируем комментарий
    sentiment = analyze_sentiment(message.text)
    bot.send_message(message.chat.id, f"Комментарий оценен как: {sentiment}")

# Хендлер для выбора режима 2
@bot.message_handler(func=lambda message: message.text == "2")
def mode_2(message):
    bot.send_message(message.chat.id, "Вы выбрали Режим 2. Отправьте ссылку на страницу с комментариями.")
    bot.register_next_step_handler(message, handle_url)

def handle_url(message):
    url = message.text
    bot.send_message(message.chat.id, "Идет сбор комментариев. Это может занять некоторое время...")

    # Получаем комментарии
    try:
        comments_data = fetch_comments(url)
        if not comments_data:
            bot.send_message(message.chat.id, "Не удалось получить комментарии. Проверьте ссылку и попробуйте снова.")
            return

        # Сохраняем данные в Excel
        file_name = "comments.xlsx"
        save_to_excel(comments_data, file_name)

        # Подсчитываем статистику по рейтингам и тональности
        positive_count = sum(1 for _, rating in comments_data if rating >= 4)
        neutral_count = sum(1 for _, rating in comments_data if rating == 3)
        negative_count = sum(1 for _, rating in comments_data if rating <= 2)

        # Подсчитываем статистику по тональности
        positive_sentiment = 0
        neutral_sentiment = 0
        negative_sentiment = 0
        for comment, _ in comments_data:
            sentiment = analyze_sentiment(comment)
            if sentiment == "Позитивный":
                positive_sentiment += 1
            elif sentiment == "Негативный":
                negative_sentiment += 1
            else:
                neutral_sentiment += 1

        # Средняя оценка
        total_ratings = sum(rating for _, rating in comments_data)
        average_rating = total_ratings / len(comments_data)

        # Отправляем файл
        with open(file_name, "rb") as file:
            bot.send_document(message.chat.id, file)

        # Отправляем статистику
        bot.send_message(
            message.chat.id,
            f"\nСредняя оценка: {average_rating:.2f}\n"
            f"Положительные отзывы (по рейтингу): {positive_count}\n"
            f"Нейтральные отзывы (по рейтингу): {neutral_count}\n"
            f"Негативные отзывы (по рейтингу): {negative_count}\n"
            f"\nТональность комментариев:\n"
            f"Позитивных: {positive_sentiment}\n"
            f"Негативных: {negative_sentiment}\n"
            f"Нейтральных: {neutral_sentiment}"
        )

        # Удаляем файл после отправки
        os.remove(file_name)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка обработки: {e}")

# Функция для отображения индикатора работы сервера в терминале
def server_status():
    symbols = ['-', '/', '|', '\\']
    while True:
        for symbol in symbols:
            sys.stdout.write(f'\rСервер работает {symbol}')
            sys.stdout.flush()
            time.sleep(0.2)

# Запуск потока с индикатором работы сервера
thread = threading.Thread(target=server_status)
thread.daemon = True
thread.start()

# Запуск бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 15 секунд...")
        time.sleep(15)
