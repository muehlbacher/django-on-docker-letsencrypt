from django.shortcuts import render
from django.conf import settings

# Create your views here.

def index(request):
        return render(request, 'index.html', {
        'media_url': settings.MEDIA_URL,
    })