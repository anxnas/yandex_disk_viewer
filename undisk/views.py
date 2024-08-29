import requests
from django.shortcuts import render, redirect
from django.views import View
from .forms import PublicLinkForm

class IndexView(View):
    def get(self, request):
        form = PublicLinkForm()
        return render(request, 'undisk/index.html', {'form': form})

    def post(self, request):
        form = PublicLinkForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data['public_key']
            response = requests.get("https://cloud-api.yandex.net/v1/disk/public/resources", params={'public_key': public_key})
            files = response.json()['_embedded']['items']
            return render(request, 'undisk/index.html', {'form': form, 'files': files, 'public_key': public_key})
        return render(request, 'undisk/index.html', {'form': form})