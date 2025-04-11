from django.http import HttpResponseForbidden
from django.template import loader

def csrf_failure(request, reason=""):
    template = loader.get_template('pages/403csrf.html')
    return HttpResponseForbidden(template.render())


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)
