from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.author} - {self.body[:30]} ...'

    def get_absolute_url(self):
        return reverse('post:post_detail', args=(self.id, self.slug))

    def likes_count(self):
        return self.pvote.count()

    def user_can_like(self, user):
        user = user.uvote.filter(post=self)
        if user.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-{self.body[:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="uvote")
    post = models.ForeignKey(Post, models.CASCADE, related_name="pvote")

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
