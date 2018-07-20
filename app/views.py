from django.shortcuts import render


def handle_404(request):
    return render(request, 'app/404.html')
