from django.contrib import admin
from django.urls import path
from recipes.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Boş URL, yani http://127.0.0.1:8000/ için home view'ını çağırır.
]
