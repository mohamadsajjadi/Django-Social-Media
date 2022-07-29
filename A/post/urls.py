from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('/<int:post_id>/<slug:slug_id>/', views.PostDetails.as_view(), name='post_detail')
]
