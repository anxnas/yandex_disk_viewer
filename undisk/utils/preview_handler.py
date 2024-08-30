import base64
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PreviewHandler:
    """
    Класс для обработки предварительного просмотра файлов.

    Attributes:
        path (str): Путь к файлу.
        file_content (bytes): Содержимое файла.
        download_link (str): Ссылка для скачивания файла.
    """
    def __init__(self, path: str, file_content: bytes, download_link: str) -> None:
        """
        Инициализация PreviewHandler.

        Args:
            path (str): Путь к файлу.
            file_content (bytes): Содержимое файла.
            download_link (str): Ссылка для скачивания файла.
        """
        self.path: str = path
        self.file_content: bytes = file_content
        self.download_link: str = download_link

    def get_preview_content(self) -> Optional[str]:
        """
        Получение содержимого для предварительного просмотра.

        Этот метод возвращает HTML-код для предварительного просмотра файла в зависимости от его типа.
        Поддерживаются изображения, видео, аудио, текстовые файлы, PDF и некоторые другие форматы.

        Returns:
            Optional[str]: HTML-код для предварительного просмотра или сообщение об ошибке.
        """
        try:
            logger.debug(f"Получение предварительного просмотра для файла: {self.path}")
            file_extension: str = self.path.split('.')[-1].lower()
            encoded_content: str = base64.b64encode(self.file_content).decode('utf-8')
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                return f'<img src="data:image/{file_extension};base64,{encoded_content}" alt="Image Preview" style="max-width: 100%;">'
            elif file_extension in ['mp4', 'webm']:
                return f'<video controls style="max-width: 100%;"><source src="data:video/{file_extension};base64,{encoded_content}" type="video/{file_extension}">Your browser does not support the video tag.</video>'
            elif file_extension in ['mp3', 'wav', 'ogg']:
                return f'<audio controls style="max-width: 100%;"><source src="data:audio/{file_extension};base64,{encoded_content}" type="audio/{file_extension}">Your browser does not support the audio element.</audio>'
            elif file_extension in ['txt', 'csv']:
                return f'<pre class="text-view">{self.file_content.decode("utf-8")}</pre>'
            elif file_extension in ['pdf']:
                return f'<embed src="data:application/pdf;base64,{encoded_content}" type="application/pdf" width="100%" height="600px" />'
            elif file_extension in ['docx', 'xlsx']:
                return self.download_link
            elif file_extension in ['zip']:
                return f'data:application/{file_extension};base64,{encoded_content}'
            else:
                return "Предварительный просмотр недоступен"
        except Exception as e:
            logger.error(f"Ошибка при получении предварительного просмотра: {e}")
            return "Предварительный просмотр недоступен"