from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from .forms import CreateUpdatePostForm, CommentCreateForm, CommentReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostDetails(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def dispatch(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['slug_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        comments = self.post_instance.pcomment.filter(is_reply=False)
        return render(request, 'post/details.html', {'post': self.post_instance, 'comments': comments, 'form': form,
                                                     'reply_form': self.form_class_reply})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment submited succesfully', 'success')
            return redirect('post:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author.id == request.user.id:
            post.delete()
            messages.success(request, "Post Deleted Succefully!", 'success')
        else:
            messages.error(request, "This post is not for you!", 'error')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_classes = CreateUpdatePostForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
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


class CommentReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted successfully!', 'success')
        return redirect('post:post_detail', post.id, post.slug)
