import requests
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from urllib.parse import quote, unquote
import io
import zipfile

from .utils.file_handler import FileHandler
from .utils.preview_handler import PreviewHandler

YANDEX_DISK_API_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"

class IndexView(View):
    def get(self, request):
        public_key = request.GET.get('public_key', '')
        path = request.GET.get('path', '')
        filter_type = request.GET.get('filter', 'all')
        sort_by = request.GET.get('sort', '-')
        sort_order = request.GET.get('order', 'asc')
        search_query = request.GET.get('search', '')
        files = []
        preview_content = ""
        download_link = ""
        if public_key:
            params = {'public_key': public_key, 'limit': 10000}
            if path:
                params['path'] = path
            response = requests.get(YANDEX_DISK_API_URL, params=params)
            files = response.json()['_embedded']['items']
            file_handler = FileHandler(files)
            files = file_handler.filter_files(filter_type)
            if sort_by != '-':
                files = file_handler.sort_files(sort_by, sort_order)
            if search_query:
                files = file_handler.search_files(search_query)
            if 'preview_path' in request.GET:
                preview_path = unquote(request.GET['preview_path'])
                download_url = f"{YANDEX_DISK_API_URL}/download"
                response = requests.get(download_url, params={'public_key': public_key, 'path': preview_path})
                if response.status_code == 200 and 'href' in response.json():
                    download_link = response.json()['href']
                    file_response = requests.get(download_link)
                    file_content = file_response.content
                    preview_handler = PreviewHandler(preview_path, file_content, download_link)
                    preview_content = preview_handler.get_preview_content()
                else:
                    preview_content = "Предварительный просмотр недоступен"
        parent_path = '/'.join(path.split('/')[:-1]) if path else ''
        return render(request, 'undisk/index.html', {'files': files, 'preview_content': preview_content, 'public_key': public_key, 'path': path, 'parent_path': parent_path, 'download_link': download_link, 'filter_type': filter_type, 'sort_by': sort_by, 'sort_order': sort_order, 'search_query': search_query})

    def post(self, request):
        if 'download_selected' in request.POST:
            selected_files = request.POST.getlist('selected_files')
            public_key = request.POST.get('public_key')
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for file_path in selected_files:
                    download_url = f"{YANDEX_DISK_API_URL}/download"
                    response = requests.get(download_url, params={'public_key': public_key, 'path': file_path})
                    if response.status_code == 200 and 'href' in response.json():
                        file_response = requests.get(response.json()['href'])
                        zip_file.writestr(file_path.split('/')[-1], file_response.content)
            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=file.zip'
            return response
        public_key = request.POST.get('public_key')
        if public_key:
            return redirect(f'?public_key={quote(public_key)}')
        return render(request, 'undisk/index.html')