import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self, files: List[Dict[str, Any]]) -> None:
        self.files: List[Dict[str, Any]] = files

    def filter_files(self, filter_type: str) -> List[Dict[str, Any]]:
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
        try:
            logger.debug(f"Сортировка файлов по: {sort_by}, порядок: {sort_order}")
            reverse: bool = (sort_order == 'desc')
            if sort_by == 'name':
                return sorted(self.files, key=lambda x: x['name'].lower(), reverse=reverse)
            elif sort_by == 'date':
                return sorted(self.files, key=lambda x: x['created'], reverse=reverse)
            elif sort_by == 'size':
                return sorted(self.files, key=lambda x: x['size'], reverse=reverse)
            else:
                return self.files
        except Exception as e:
            logger.error(f"Ошибка при сортировке файлов: {e}")
            return []

    def search_files(self, search_query: str) -> List[Dict[str, Any]]:
        try:
            logger.debug(f"Поиск файлов по запросу: {search_query}")
            return [file for file in self.files if search_query.lower() in file['name'].lower()]
        except Exception as e:
            logger.error(f"Ошибка при поиске файлов: {e}")
            return []