from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounting/', include('accounting.urls')),
                  path('', include('homeService.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
