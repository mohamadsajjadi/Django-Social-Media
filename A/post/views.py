from django.shortcuts import render
from django.views import View
from .models import Post


class PostDetails(View):
    def get(self, request, post_id, slug_id):
        post = Post.objects.get(pk=post_id, slug=slug_id)
        return render(request, 'post/details.html', {'post': post})
