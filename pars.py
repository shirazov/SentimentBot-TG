from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
import os
import time
import random

def fetch_comments(url):
    try:
        # Настройка Selenium WebDriver
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.headless = True  # Запуск без отображения браузера
        service = Service("chromedriver.exe")  # Укажите путь к ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)

        # Открытие страницы
        driver.get(url)
        time.sleep(random.uniform(3, 6))  # Задержка для имитации поведения пользователя

        # Извлечение блоков отзывов
        review_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-uuid]')
        data = []

        for review_block in review_blocks:
            try:
                # Извлечение текста комментария
                comment_element = review_block.find_element(By.CSS_SELECTOR, 'span.zq6_30')
                comment_text = comment_element.text.strip()

                # Извлечение рейтинга
                try:
                    stars_elements = review_block.find_elements(By.CSS_SELECTOR, 'svg[style*="rgba(255, 168, 0"]')
                    rating = len(stars_elements)  # Количество звезд определяется по найденным элементам

                    # Диагностика
                    print(f"Комментарий: {comment_text}")
                    print(f"Рейтинг: {rating}")
                except Exception as e:
                    print(f"Ошибка при извлечении рейтинга: {e}")
                    rating = 0  # Если не удалось найти оценку

                data.append((comment_text, rating))
            except Exception as e:
                print(f"Ошибка при обработке блока отзыва: {e}")

        driver.quit()  # Закрытие браузера
        return data

    except Exception as e:
        print(f"Ошибка при извлечении комментариев: {e}")
        if 'driver' in locals():
            driver.quit()
        return None


def save_to_excel(data, file_name="comments.xlsx"):
    try:
        # Проверяем, не занят ли файл, и удаляем его, если он существует
        if os.path.exists(file_name):
            print(f"Файл {file_name} уже существует. Удаляю его.")
            os.remove(file_name)

        # Создаем Excel-файл
        wb = Workbook()
        ws = wb.active
        ws.title = "Комментарии"
        
        # Заполняем заголовки
        ws.append(["Комментарий", "Оценка", "Категория"])
        
        # Заполняем данные
        for comment, rating in data:
            if rating in [1, 2]:
                category = "Негативный"
            elif rating == 3:
                category = "Нейтральный"
            else:
                category = "Положительный"
            ws.append([comment, rating, category])
        
        # Сохраняем файл
        wb.save(file_name)
        print(f"Данные успешно сохранены в файл {file_name}")
        print(f"Полный путь к файлу: {os.path.abspath(file_name)}")
    except PermissionError:
        print(f"Ошибка: Нет доступа к файлу {file_name}. Убедитесь, что файл не открыт.")
    except Exception as e:
        print(f"Ошибка сохранения в Excel: {e}")


def calculate_average_rating(data):
    if not data:
        print("Нет данных для вычисления средней оценки.")
        return

    total_ratings = sum(rating for _, rating in data)
    average_rating = total_ratings / len(data)
    print(f"\nСредняя оценка: {average_rating:.2f}")

    # Подсчет отзывов по категориям
    negative = sum(1 for _, rating in data if rating in [1, 2])
    neutral = sum(1 for _, rating in data if rating == 3)
    positive = sum(1 for _, rating in data if rating in [4, 5])

    print(f"Негативные отзывы: {negative}")
    print(f"Нейтральные отзывы: {neutral}")
    print(f"Положительные отзывы: {positive}")


def main():
    url = input("Введите ссылку на страницу с комментариями: ").strip()
    comments_data = fetch_comments(url)
    
    if comments_data:
        save_to_excel(comments_data)
        calculate_average_rating(comments_data)
    else:
        print("Не удалось получить данные о комментариях.")


if __name__ == "__main__":
    main()
