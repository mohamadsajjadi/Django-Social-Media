from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('<int:post_id>/<slug:slug_id>/', views.PostDetails.as_view(), name='post_detail'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('create/', views.CreatePostView.as_view(), name='post_create'),
    path('reply/<int:post_id>/<int:comment_id>/', views.CommentReplyView.as_view(), name='add_reply')
]
