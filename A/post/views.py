from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from .forms import CreateUpdatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify


class PostDetails(View):
    def get(self, request, post_id, slug_id):
        post = Post.objects.get(pk=post_id, slug=slug_id)
        return render(request, 'post/details.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.author.id == request.user.id:
            post.delete()
            messages.success(request, "Post Deleted Succefully!", 'success')
        else:
            messages.error(request, "This post is not for you!", 'error')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_classes = CreateUpdatePostForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.author.id:
            messages.error(request, 'You can update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_classes(instance=post)
        return render(request, 'post/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_classes(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post updated succesfully!', 'success')
            return redirect('post:post_detail', post.id, post.slug)


class CreatePostView(LoginRequiredMixin, View):
    form_classes = CreateUpdatePostForm

    def get(self, request, *args, **kwargs):
        form = self.form_classes()
        return render(request, 'post/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_classes(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post successfully added to your profile', 'success')
            return redirect('post:post_detail', new_post.id, new_post.slug)
