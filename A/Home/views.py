from django.shortcuts import render
from django.views import View


def home(request):
    return render(request, 'Home/index.html')


class Homeview(View):
    def get(self, request):
        return render(request, 'Home/index.html')

    def post(self, request):
        return render(request, 'Home/index.html')
