from django.shortcuts import render
from django.views import View
from post.models import Post


def home(request):
    return render(request, 'Home/index.html')


class Homeview(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'Home/index.html', {'post': posts})
