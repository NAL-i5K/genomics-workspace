from django.shortcuts import render


def handle_404(request, exception):
    return render(request, 'app/404.html')
