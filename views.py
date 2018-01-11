from django.http import HttpResponse

# setup urls/routing and views


def home_view(request):
    return HttpResponse('<h1>Hello from django and up modules!</h1>')
