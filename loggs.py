# Удаляем стандартный обработчик
from loguru import logger


logger.remove()
# Настраиваем логирование в файл с ограничением количества файлов
logger.add(
    "loggs.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="5 MB",  # Ротация файла каждые 10 MB
    retention="10 days",  # Хранить только 5 последних логов
    compression="zip",  # Сжимать старые логи в архив
    backtrace=True,     # Сохранение трассировки ошибок
    diagnose=True       # Подробный вывод
)