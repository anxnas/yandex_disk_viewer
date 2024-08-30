import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FileHandler:
    """
    Класс для обработки файлов.

    Attributes:
        files (List[Dict[str, Any]]): Список файлов.
    """
    def __init__(self, files: List[Dict[str, Any]]) -> None:
        """
        Инициализация FileHandler.

        Args:
            files (List[Dict[str, Any]]): Список файлов.
        """
        self.files: List[Dict[str, Any]] = files

    def filter_files(self, filter_type: str) -> List[Dict[str, Any]]:
        """
        Фильтрация файлов по типу.

        Этот метод фильтрует файлы по заданному типу, например, документы, изображения, видео и аудио.

        Args:
            filter_type (str): Тип фильтрации (all, documents, images, videos, audio).

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список файлов.
        """
        try:
            logger.debug(f"Фильтрация файлов по типу: {filter_type}")
            if filter_type == 'all':
                return self.files
            elif filter_type == 'documents':
                return [file for file in self.files if file['name'].split('.')[-1].lower() in ['doc', 'docx', 'pdf', 'txt', 'xlsx', 'csv']]
            elif filter_type == 'images':
                return [file for file in self.files if file['name'].split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'gif']]
            elif filter_type == 'videos':
                return [file for file in self.files if file['name'].split('.')[-1].lower() in ['mp4', 'webm']]
            elif filter_type == 'audio':
                return [file for file in self.files if file['name'].split('.')[-1].lower() in ['mp3', 'wav', 'ogg']]
            else:
                return self.files
        except Exception as e:
            logger.error(f"Ошибка при фильтрации файлов: {e}")
            return []

    def sort_files(self, sort_by: str, sort_order: str) -> List[Dict[str, Any]]:
        """
        Сортировка файлов.

        Этот метод сортирует файлы по заданному полю и порядку.

        Args:
            sort_by (str): Поле для сортировки (name, date, size).
            sort_order (str): Порядок сортировки (asc или desc).

        Returns:
            List[Dict[str, Any]]: Отсортированный список файлов.
        """
        try:
            logger.debug(f"Сортировка файлов по: {sort_by}, порядок: {sort_order}")
            reverse: bool = (sort_order == 'desc')
            if sort_by == 'name':
                return sorted(self.files, key=lambda x: x['name'].lower(), reverse=reverse)
            elif sort_by == 'date':
                return sorted(self.files, key=lambda x: x['created'], reverse=reverse)
            elif sort_by == 'size':
                return sorted(self.files, key=lambda x: x.get('size', float('-inf')), reverse=reverse)
            else:
                return self.files
        except Exception as e:
            logger.error(f"Ошибка при сортировке файлов: {e}")
            return []

    def search_files(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Поиск файлов по запросу.

        Этот метод выполняет поиск файлов по заданному запросу.

        Args:
            search_query (str): Поисковый запрос.

        Returns:
            List[Dict[str, Any]]: Список файлов, соответствующих запросу.
        """
        try:
            logger.debug(f"Поиск файлов по запросу: {search_query}")
            return [file for file in self.files if search_query.lower() in file['name'].lower()]
        except Exception as e:
            logger.error(f"Ошибка при поиске файлов: {e}")
            return []