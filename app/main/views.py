from django.shortcuts import render, HttpResponse
# Create your views here.


def temp(request):
    return render(request, 'with_nav.html')
