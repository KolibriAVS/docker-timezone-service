# Мировое время (Timezone)

Многокомпонентное приложение с использованием Docker Compose для преобразования времени между часовыми поясами.

## Структура проекта
- **Frontend:** HTML/JS/Tailwind CSS (Nginx)
- **Backend:** FastAPI (Python)
- **Web-Service:** FastAPI (Python) + pytz (Эмулятор внешнего сервиса)
- **Database:** PostgreSQL

## Запуск проекта
1. Убедитесь, что у вас установлен Docker и плагин Docker Compose.
2. В корневой директории проекта выполните команду:
   ```bash
   docker compose up -d
3. Откройте интерфейс в браузере по адресу: http://localhost:8080