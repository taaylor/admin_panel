# Количество воркеров (процессов), обрабатывающих запросы
workers = 4

# Количество потоков на каждый воркер
threads = 10

# Какой хост и порт будет слушать Gunicorn
bind = "0.0.0.0:8000"

# Таймаут для обработки запроса (в секундах)
timeout = 30

# Очередь входящих запросов перед обработкой
backlog = 512

# Сколько запросов обработает воркер перед перезапуском
max_requests = 1000

# Разброс количества запросов до перезапуска воркера
# Если max_requests = 1000, то воркеры перезапустятся случайно после 950-1050 запросов
# Это предотвращает одновременный перезапуск всех воркеров
max_requests_jitter = 50
