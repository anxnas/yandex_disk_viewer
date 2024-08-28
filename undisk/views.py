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
            return redirect('index')  # Перенаправление на ту же страницу с параметром public_key
        return render(request, 'undisk/index.html', {'form': form})