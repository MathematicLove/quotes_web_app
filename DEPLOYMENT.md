# Инструкция по развертыванию приложения "Сборник цитат"

## Вариант 1: Развертывание на Render.com (Рекомендуется)

### Шаги:

1. **Зарегистрируйтесь на [Render.com](https://render.com)**
   - Создайте аккаунт (можно через GitHub)

2. **Подготовьте проект**
   - Убедитесь, что все файлы закоммичены в Git
   - Убедитесь, что репозиторий доступен на GitHub/GitLab

3. **Создайте новый Web Service на Render**
   - Нажмите "New +" → "Web Service"
   - Подключите ваш Git репозиторий
   - Выберите ветку (обычно `main` или `master`)

4. **Настройте сервис:**
   - **Name**: `quotes-app` (или любое другое)
   - **Environment**: `Python 3`
   - **Build Command**: `cd src && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `cd src && gunicorn quotes_project.wsgi:application --bind 0.0.0.0:$PORT`

5. **Добавьте переменные окружения:**
   - `DJANGO_SECRET_KEY` - оставьте пустым (Render сгенерирует автоматически)
   - `DJANGO_DEBUG` = `false`
   - `ALLOWED_HOSTS` = `.onrender.com`

6. **Создайте базу данных:**
   - Нажмите "New +" → "PostgreSQL"
   - Выберите план "Free"
   - Скопируйте `DATABASE_URL` из настроек базы
   - Добавьте эту переменную в ваш Web Service

7. **Запустите развертывание:**
   - Нажмите "Create Web Service"
   - Дождитесь завершения сборки (5-10 минут)

8. **Создайте суперпользователя:**
   - После успешного развертывания откройте консоль
   - Выполните: `python manage.py createsuperuser`

### Результат:
Ваше приложение будет доступно по адресу: `https://your-app-name.onrender.com`

---

## Вариант 2: Развертывание на Railway.app

### Шаги:

1. **Зарегистрируйтесь на [Railway.app](https://railway.app)**
   - Подключите GitHub аккаунт

2. **Создайте новый проект:**
   - Нажмите "New Project" → "Deploy from GitHub repo"
   - Выберите ваш репозиторий

3. **Добавьте PostgreSQL:**
   - Нажмите "New" → "Database" → "PostgreSQL"
   - Railway автоматически добавит `DATABASE_URL`

4. **Настройте переменные окружения:**
   - `DJANGO_DEBUG` = `false`
   - `DJANGO_SECRET_KEY` = сгенерируйте случайную строку

5. **Запустите развертывание:**
   - Railway автоматически определит Python проект
   - Выполнит `pip install -r requirements.txt`
   - Запустит приложение

---

## Вариант 3: Развертывание на Heroku

### Шаги:

1. **Установите Heroku CLI**
2. **Создайте приложение:**
   ```bash
   heroku create your-app-name
   ```

3. **Добавьте PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Настройте переменные:**
   ```bash
   heroku config:set DJANGO_DEBUG=false
   heroku config:set DJANGO_SECRET_KEY=your-secret-key
   ```

5. **Разверните:**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

## Вариант 4: Локальное развертывание с Docker

### Шаги:

1. **Убедитесь, что установлен Docker и Docker Compose**

2. **Перейдите в папку deploy:**
   ```bash
   cd deploy
   ```

3. **Создайте файл .env:**
   ```bash
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=1
   POSTGRES_DB=quotes_db
   POSTGRES_USER=ayzek
   POSTGRES_PASSWORD=123
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=admin123
   ```

4. **Запустите контейнеры:**
   ```bash
   docker-compose up -d
   ```

5. **Создайте суперпользователя:**
   ```bash
   docker exec deploy-web-1 python manage.py createsuperuser
   ```

6. **Откройте приложение:**
   - http://localhost:8000

---

## Проверка работоспособности

После развертывания проверьте:

1. **Главная страница** - должна показывать случайную цитату
2. **Админка** - `/admin/` должна открываться
3. **API** - `/api/random/` должен возвращать JSON
4. **Поиск** - `/search/` должен работать
5. **Топ цитат** - `/top/` должен показывать рейтинг

## Возможные проблемы

### Ошибка "no module named 'dj_database_url'"
- Убедитесь, что `dj-database-url==2.1.0` добавлен в requirements.txt

### Ошибка "database connection failed"
- Проверьте переменную `DATABASE_URL`
- Убедитесь, что база данных создана и доступна

### Статические файлы не загружаются
- Проверьте, что выполнился `python manage.py collectstatic`
- Убедитесь, что `STATIC_ROOT` настроен правильно

### Ошибка миграций
- Выполните `python manage.py migrate` вручную
- Проверьте логи развертывания

## Полезные команды

```bash
# Проверка статуса приложения
curl https://your-app.onrender.com/healthcheck/

# Проверка API
curl https://your-app.onrender.com/api/random/

# Просмотр логов (если доступно)
heroku logs --tail  # для Heroku
railway logs        # для Railway
```

## Ссылка для демонстрации

После успешного развертывания вы получите URL вида:
- Render: `https://your-app-name.onrender.com`
- Railway: `https://your-app-name.railway.app`
- Heroku: `https://your-app-name.herokuapp.com`

Эту ссылку можно отправить другому человеку для демонстрации работы приложения.
