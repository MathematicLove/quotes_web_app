#!/bin/bash

echo "🚀 Подготовка к развертыванию на Render.com"
echo "=============================================="

# Проверяем, что мы в корневой папке проекта
if [ ! -f "README.md" ]; then
    echo "❌ Ошибка: Запустите скрипт из корневой папки проекта"
    exit 1
fi

# Проверяем Git статус
if [ ! -d ".git" ]; then
    echo "❌ Ошибка: Это не Git репозиторий"
    echo "Выполните: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# Проверяем, что все изменения закоммичены
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Внимание: Есть незакоммиченные изменения"
    echo "Выполните: git add . && git commit -m 'Update for deployment'"
    read -p "Продолжить? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ Проект готов к развертыванию"
echo ""
echo "📋 Следующие шаги:"
echo "1. Перейдите на https://render.com"
echo "2. Создайте аккаунт (можно через GitHub)"
echo "3. Нажмите 'New +' → 'Web Service'"
echo "4. Подключите ваш Git репозиторий"
echo "5. Настройте сервис:"
echo "   - Name: quotes-app"
echo "   - Environment: Python 3"
echo "   - Build Command: cd src && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
echo "   - Start Command: cd src && gunicorn quotes_project.wsgi:application --bind 0.0.0.0:\$PORT"
echo ""
echo "6. Создайте PostgreSQL базу данных:"
echo "   - New + → PostgreSQL → Free"
echo "   - Скопируйте DATABASE_URL"
echo "   - Добавьте в переменные окружения Web Service"
echo ""
echo "7. Добавьте переменные окружения:"
echo "   - DJANGO_DEBUG = false"
echo "   - ALLOWED_HOSTS = .onrender.com"
echo ""
echo "8. Нажмите 'Create Web Service'"
echo "9. Дождитесь завершения сборки (5-10 минут)"
echo "10. Создайте суперпользователя через консоль:"
echo "    python manage.py createsuperuser"
echo ""
echo "🎯 После развертывания ваше приложение будет доступно по адресу:"
echo "   https://your-app-name.onrender.com"
echo ""
echo "📚 Подробная инструкция в файле DEPLOYMENT.md"
echo ""
echo "🔗 Ссылку на развернутое приложение можно отправить другому человеку!"
