import requests
from django.shortcuts import render, redirect
from django.views import View
from .forms import PublicLinkForm
import base64
from urllib.parse import quote, unquote

YANDEX_DISK_API_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"

class IndexView(View):
    def get(self, request):
        form = PublicLinkForm()
        public_key = request.GET.get('public_key', '')
        path = request.GET.get('path', '')
        files = []
        preview_content = ""
        if public_key:
            params = {'public_key': public_key, 'limit': 10000}
            if path:
                params['path'] = path
            response = requests.get(YANDEX_DISK_API_URL, params=params)
            files = response.json()['_embedded']['items']
            if 'preview_path' in request.GET:
                preview_path = unquote(request.GET['preview_path'])
                download_url = f"{YANDEX_DISK_API_URL}/download"
                response = requests.get(download_url, params={'public_key': public_key, 'path': preview_path})
                if response.status_code == 200 and 'href' in response.json():
                    download_link = response.json()['href']
                    file_response = requests.get(download_link)
                    file_content = file_response.content
                    preview_content = self.get_preview_content(preview_path, file_content)
                else:
                    preview_content = "Предварительный просмотр недоступен"
        return render(request, 'undisk/index.html', {'form': form, 'files': files, 'preview_content': preview_content, 'public_key': public_key, 'path': path})

    def post(self, request):
        form = PublicLinkForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data['public_key']
            return redirect(f'?public_key={quote(public_key)}')
        return render(request, 'undisk/index.html', {'form': form})

    def get_preview_content(self, path, file_content):
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
        elif file_extension in ['docx', 'xlsx', 'zip']:
            return f'data:application/{file_extension};base64,{encoded_content}'
        else:
            return "Предварительный просмотр недоступен"