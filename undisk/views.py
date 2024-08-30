import requests
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from urllib.parse import quote, unquote
import base64
import zipfile
import io

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
            files = self.filter_files(files, filter_type)
            if sort_by != '-':
                files = self.sort_files(files, sort_by, sort_order)
            if search_query:
                files = self.search_files(files, search_query)
            if 'preview_path' in request.GET:
                preview_path = unquote(request.GET['preview_path'])
                download_url = f"{YANDEX_DISK_API_URL}/download"
                response = requests.get(download_url, params={'public_key': public_key, 'path': preview_path})
                if response.status_code == 200 and 'href' in response.json():
                    download_link = response.json()['href']
                    file_response = requests.get(download_link)
                    file_content = file_response.content
                    preview_content = self.get_preview_content(preview_path, file_content, download_link)
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

    def get_preview_content(self, path, file_content, download_link):
        file_extension = path.split('.')[-1].lower()
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            return f'<img src="data:image/{file_extension};base64,{encoded_content}" alt="Image Preview">'
        elif file_extension in ['mp4', 'webm']:
            return f'<video controls><source src="data:video/{file_extension};base64,{encoded_content}" type="video/{file_extension}">Your browser does not support the video tag.</video>'
        elif file_extension in ['mp3', 'wav', 'ogg']:
            return f'<audio controls><source src="data:audio/{file_extension};base64,{encoded_content}" type="audio/{file_extension}">Your browser does not support the audio element.</audio>'
        elif file_extension in ['txt', 'csv']:
            return f'<pre class="text-view">{file_content.decode("utf-8")}</pre>'
        elif file_extension in ['pdf']:
            return f'<embed src="data:application/pdf;base64,{encoded_content}" type="application/pdf" width="100%" height="600px" />'
        elif file_extension in ['docx', 'xlsx']:
            return download_link
        elif file_extension in ['zip']:
            return f'data:application/{file_extension};base64,{encoded_content}'
        else:
            return "Предварительный просмотр недоступен"

    def filter_files(self, files, filter_type):
        if filter_type == 'all':
            return files
        elif filter_type == 'documents':
            return [file for file in files if file['name'].split('.')[-1].lower() in ['doc', 'docx', 'pdf', 'txt', 'xlsx', 'csv']]
        elif filter_type == 'images':
            return [file for file in files if file['name'].split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'gif']]
        elif filter_type == 'videos':
            return [file for file in files if file['name'].split('.')[-1].lower() in ['mp4', 'webm']]
        elif filter_type == 'audio':
            return [file for file in files if file['name'].split('.')[-1].lower() in ['mp3', 'wav', 'ogg']]
        else:
            return files

    def sort_files(self, files, sort_by, sort_order):
        reverse = (sort_order == 'desc')
        if sort_by == 'name':
            return sorted(files, key=lambda x: x['name'].lower(), reverse=reverse)
        elif sort_by == 'date':
            return sorted(files, key=lambda x: x['created'], reverse=reverse)
        elif sort_by == 'size':
            return sorted(files, key=lambda x: x['size'], reverse=reverse)
        else:
            return files

    def search_files(self, files, search_query):
        return [file for file in files if search_query.lower() in file['name'].lower()]