# YaCut

Сервис укорачивания ссылок с возможностью асинхронной загрузки файлов на Яндекс Диск.

## Возможности

-   Генерация коротких ссылок (автоматическая или пользовательский вариант)
-   Переадресация по коротким ссылкам на оригинальные URL
-   Асинхронная загрузка нескольких файлов на Яндекс Диск
-   REST API для программного взаимодействия
-   Валидация входных данных и обработка ошибок

## Стек технологий

-   **Backend:** Python 3.12, Flask 3.0
-   **База данных:** SQLite, SQLAlchemy 2.0, Flask-Migrate
-   **Формы:** Flask-WTF, WTForms
-   **Асинхронность:** aiohttp (для работы с API Яндекс Диска)
-   **Тестирование:** pytest, pytest-aiohttp
-   **Документация API:** OpenAPI 3.0

Установка и запуск.

1. Клонирование репозитория

```bash
git clone <URL_репозитория>
cd yacut

2. Создание виртуального окружения
Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

3. Установка зависимостей

pip install -r requirements.txt

4. Настройка переменных окружения
Создайте файл .env в корне проекта:

FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_oauth_token

5. Инициализация базы данных

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

6. Запуск приложения

flask run

Приложение будет доступно по адресу: http://127.0.0.1:5000/
Использование
Веб-интерфейс
Главная страница (/): создание коротких ссылок
Загрузка файлов (/files): асинхронная загрузка файлов на Яндекс Диск
API
Создание короткой ссылки

POST /api/id/
Content-Type: application/json

{
  "url": "https://example.com/very-long-url",
  "custom_id": "mylink"  // опционально
}

Ответ (201 Created):

{
  "url": "https://example.com/very-long-url",
  "short_link": "http://127.0.0.1:5000/mylink"
}

Получение оригинальной ссылки
GET /api/id/{short_id}/

Ответ (200 OK):
{
  "url": "https://example.com/very-long-url"
}
