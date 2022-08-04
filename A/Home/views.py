from django.shortcuts import render
from django.views import View
from post.models import Post
from post.forms import PostSearchForm


class Homeview(View):
    form_class = PostSearchForm

    def get(self, request):
        search_text = request.GET.get('search')
        posts = Post.objects.all()
        if search_text:
            posts = Post.objects.filter(body__contains=request.GET['search'])
        return render(request, 'Home/index.html', {'post': posts, 'form': self.form_class})
