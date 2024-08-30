import logging
from logging.handlers import RotatingFileHandler
import os

class LogConfig:
    """
    Класс для настройки логирования.

    Attributes:
        log_file_name (str): Имя файла для логов.
        max_bytes (int): Максимальный размер файла логов в байтах.
        backup_count (int): Количество резервных копий файлов логов.
        encoding (str): Кодировка файла логов.
        level (int): Уровень логирования.
    """
    def __init__(self, log_file_name: str, max_bytes: int = 100*1024*1024, backup_count: int = 5, encoding: str = 'utf-8', level: int = logging.INFO):
        """
        Инициализация LogConfig.

        Args:
            log_file_name (str): Имя файла для логов.
            max_bytes (int): Максимальный размер файла логов в байтах.
            backup_count (int): Количество резервных копий файлов логов.
            encoding (str): Кодировка файла логов.
            level (int): Уровень логирования.
        """
        self.log_file_name: str = log_file_name
        self.max_bytes: int = max_bytes
        self.backup_count: int = backup_count
        self.encoding: str = encoding
        self.level: int = level

        # Создание директории, если она не существует
        log_dir: str = os.path.dirname(log_file_name)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def setup_logging(self) -> None:
        """
        Настройка логирования.

        Этот метод настраивает логирование, создавая обработчик логов с ротацией файлов,
        устанавливая формат логов и добавляя обработчик к основному логгеру.
        """
        logger = logging.getLogger()
        handler = RotatingFileHandler(self.log_file_name, maxBytes=self.max_bytes, backupCount=self.backup_count, encoding=self.encoding)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.level)