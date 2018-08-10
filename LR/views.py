from django.http import HttpResponse

def Home(request):
    return HttpResponse('<a href="permits/">permits</a>')
