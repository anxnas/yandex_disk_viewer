import requests
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpRequest
from urllib.parse import quote, unquote
import io
import zipfile
import logging
from typing import List, Dict, Any

from .utils.file_handler import FileHandler
from .utils.preview_handler import PreviewHandler
from .utils.log_config import LogConfig

# Настройка логирования
log_config = LogConfig(log_file_name='log/undisk.log', level=logging.DEBUG)
log_config.setup_logging()
logger = logging.getLogger(__name__)

YANDEX_DISK_API_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"

class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logger.debug("GET запрос получен")
        try:
            public_key: str = request.GET.get('public_key', '')
            path: str = request.GET.get('path', '')
            filter_type: str = request.GET.get('filter', 'all')
            sort_by: str = request.GET.get('sort', '-')
            sort_order: str = request.GET.get('order', 'asc')
            search_query: str = request.GET.get('search', '')
            files: List[Dict[str, Any]] = []
            preview_content: str = ""
            download_link: str = ""
            if public_key:
                logger.debug(f"Получен public_key: {public_key}")
                params: Dict[str, Any] = {'public_key': public_key, 'limit': 10000}
                if path:
                    params['path'] = path
                response: requests.Response = requests.get(YANDEX_DISK_API_URL, params=params)
                response.raise_for_status()
                files = response.json()['_embedded']['items']
                file_handler = FileHandler(files)
                files = file_handler.filter_files(filter_type)
                if sort_by != '-':
                    files = file_handler.sort_files(sort_by, sort_order)
                if search_query:
                    files = file_handler.search_files(search_query)
                if 'preview_path' in request.GET:
                    preview_path: str = unquote(request.GET['preview_path'])
                    download_url: str = f"{YANDEX_DISK_API_URL}/download"
                    response = requests.get(download_url, params={'public_key': public_key, 'path': preview_path})
                    response.raise_for_status()
                    if 'href' in response.json():
                        download_link = response.json()['href']
                        file_response: requests.Response = requests.get(download_link)
                        file_response.raise_for_status()
                        file_content: bytes = file_response.content
                        preview_handler = PreviewHandler(preview_path, file_content, download_link)
                        preview_content = preview_handler.get_preview_content()
                    else:
                        preview_content = "Предварительный просмотр недоступен"
            parent_path: str = '/'.join(path.split('/')[:-1]) if path else ''
            logger.info("GET запрос успешно обработан")
            return render(request, 'undisk/index.html', {'files': files, 'preview_content': preview_content, 'public_key': public_key, 'path': path, 'parent_path': parent_path, 'download_link': download_link, 'filter_type': filter_type, 'sort_by': sort_by, 'sort_order': sort_order, 'search_query': search_query})
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к Yandex Disk API: {e}")
            return HttpResponse("Произошла ошибка при запросе к Yandex Disk API.", status=500)
        except Exception as e:
            logger.critical(f"Неизвестная ошибка при обработке GET запроса: {e}")
            return HttpResponse("Произошла неизвестная ошибка при обработке запроса.", status=500)

    def post(self, request: HttpRequest) -> HttpResponse:
        logger.debug("POST запрос получен")
        try:
            if 'download_selected' in request.POST:
                selected_files: List[str] = request.POST.getlist('selected_files')
                public_key: str = request.POST.get('public_key')
                zip_buffer: io.BytesIO = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for file_path in selected_files:
                        download_url: str = f"{YANDEX_DISK_API_URL}/download"
                        response: requests.Response = requests.get(download_url, params={'public_key': public_key, 'path': file_path})
                        response.raise_for_status()
                        if 'href' in response.json():
                            file_response: requests.Response = requests.get(response.json()['href'])
                            file_response.raise_for_status()
                            zip_file.writestr(file_path.split('/')[-1], file_response.content)
                zip_buffer.seek(0)
                response: HttpResponse = HttpResponse(zip_buffer, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename=file.zip'
                logger.info("Файлы успешно загружены в zip архив")
                return response
            public_key = request.POST.get('public_key')
            if public_key:
                logger.debug(f"Получен public_key: {public_key}")
                return redirect(f'?public_key={quote(public_key)}')
            logger.info("POST запрос успешно обработан")
            return render(request, 'undisk/index.html')
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к Yandex Disk API: {e}")
            return HttpResponse("Произошла ошибка при запросе к Yandex Disk API.", status=500)
        except Exception as e:
            logger.critical(f"Неизвестная ошибка при обработке POST запроса: {e}")
            return HttpResponse("Произошла неизвестная ошибка при обработке запроса.", status=500)