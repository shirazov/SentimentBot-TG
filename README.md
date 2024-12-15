# SentimentBot-TG

**Project Description:**
SentimentBot-TG is a powerful Telegram bot designed for sentiment analysis of reviews. The bot is based on a pre-trained model that has been refined and optimized for sentiment analysis tasks. The project offers two main modes of operation:

### Modes of Operation
1. **Single Comment Analysis**
   Users can input a single comment to instantly determine its sentiment (positive, negative, or neutral).

2. **Review Analysis from Product Link**
   Users provide a product link from Ozon. The bot parses all reviews for the product, analyzes them, and generates a detailed report:

   - **Average Product Rating**
   - **Number of Positive, Neutral, and Negative Reviews (by rating)**
   - **Comment Sentiment Analysis (model-based)**
   - **Top Positive Aspects**
   - **Top Negative Aspects**

   Additionally, the bot sends an Excel file (XLSX) containing all comments and their ratings.

### Features
- Utilizes a pre-trained neural network, fine-tuned to improve sentiment analysis accuracy.
- Enables direct data processing from Telegram.
- Supports review history storage using a database.
- Provides user-friendly report formats.

### Installation and Launch
To launch the Telegram bot, follow these steps:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the bot:
   ```bash
   python bot.py
   ```

### Note
SentimentBot-TG is under development. Functionality and features may change. If you encounter any issues or have suggestions, please let us know!

### Applications
SentimentBot-TG is a convenient tool for review analysis and can be beneficial for:
- Marketers studying product reviews.
- E-commerce store owners monitoring product quality.
- Users wanting to quickly understand the sentiment of product reviews before making a purchase.

Discover the simplicity and power of SentimentBot-TG! 🚀

---

# SentimentBot-TG

**Описание проекта:**
SentimentBot-TG — это мощный Telegram-бот для анализа тональности отзывов. Бот построен на базе предварительно обученной модели, которая была доработана и оптимизирована для решения задач анализа тональности. Проект предоставляет два основных режима работы:

### Режимы работы
1. **Анализ отдельного комментария**
   Пользователь может ввести один комментарий, чтобы мгновенно получить его тональность (положительный, отрицательный или нейтральный).

2. **Анализ отзывов по ссылке на товар**
   Пользователь отправляет ссылку на товар с Ozon, бот парсит все отзывы к этому товару, анализирует их и предоставляет подробный отчет:

   - **Средняя оценка товара**
   - **Количество положительных, нейтральных и негативных отзывов (по рейтингу)**
   - **Тональность комментариев (анализ модели)**
   - **Топ положительных аспектов**
   - **Топ отрицательных аспектов**

   В дополнение к текстовому отчету бот отправляет Excel-файл (XLSX) со всеми комментариями и их оценками.

### Особенности
- Использование предварительно обученной нейронной сети, доработанной для улучшения качества анализа тональности.
- Возможность обработки данных напрямую из Telegram.
- Поддержка работы с историей отзывов с использованием базы данных.
- Удобный формат отчетов для пользователей.

### Установка и запуск
Для запуска Telegram-бота выполните следующие шаги:

1. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите бота:
   ```bash
   python bot.py
   ```

### Примечание
SentimentBot-TG находится в разработке. Возможны изменения в функциональности и работе бота. Если вы обнаружили ошибку или у вас есть предложения, пожалуйста, дайте знать!

### Применение
SentimentBot-TG — это удобный инструмент для анализа отзывов, который может быть полезен:
- Маркетологам для исследования отзывов о продуктах.
- Владельцам интернет-магазинов для мониторинга качества товаров.
- Пользователям, которые хотят быстро понять тональность отзывов о товаре перед покупкой.

Оцените простоту и мощность SentimentBot-TG! 🚀

