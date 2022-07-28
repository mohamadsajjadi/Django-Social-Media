from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls',namespace='home')),
    path('account/', include('account.urls',namespace='account'))
]
