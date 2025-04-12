from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.template import loader


def csrf_failure(request, reason=""):
    return render(request, 'pages/403csrf.html')


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'pages/403.html', status=403)
