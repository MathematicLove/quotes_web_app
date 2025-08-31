#!/bin/bash

echo "🚀 Настройка GitHub репозитория"
echo "================================"

# Проверяем, что мы в Git репозитории
if [ ! -d ".git" ]; then
    echo "❌ Ошибка: Это не Git репозиторий"
    exit 1
fi

echo "✅ Git репозиторий найден"
echo ""

echo "📋 Следующие шаги:"
echo "1. Перейдите на https://github.com"
echo "2. Нажмите 'New repository'"
echo "3. Название: quotes_web_app"
echo "4. Оставьте публичным"
echo "5. НЕ инициализируйте с README"
echo "6. Нажмите 'Create repository'"
echo ""

read -p "Создали репозиторий на GitHub? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔗 Введите URL вашего GitHub репозитория:"
    echo "Пример: https://github.com/username/quotes_web_app.git"
    read -p "URL: " github_url
    
    if [ -n "$github_url" ]; then
        echo ""
        echo "🔧 Настраиваю remote origin..."
        git remote add origin "$github_url"
        
        echo "🔄 Переименовываю ветку в main..."
        git branch -M main
        
        echo "📤 Отправляю код на GitHub..."
        git push -u origin main
        
        echo ""
        echo "✅ Готово! Репозиторий настроен и код отправлен."
        echo "🔗 Ваш репозиторий: $github_url"
        echo ""
        echo "🎯 Теперь можно развертывать на Render.com!"
        echo "Запустите: ./deploy-render.sh"
    else
        echo "❌ URL не введен"
    fi
else
    echo "❌ Сначала создайте репозиторий на GitHub"
fi
