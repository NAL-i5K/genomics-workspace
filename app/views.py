from django.shortcuts import render
from django.http import HttpRequest


def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html', {
            'title': 'Home Page',
        })


def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html', {
            'title': 'Contact',
            'message': 'National Agricultural Library',
        })


def handle_404(request):
    return render(request, 'app/404.html')
