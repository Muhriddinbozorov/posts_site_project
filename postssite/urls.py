from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import main_page

urlpatterns = [
    path("", main_page, name="main_page"),
    path('users/', include("users.urls")),
    path("posts/", include("posts.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)