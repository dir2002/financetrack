
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('transactions/', include('transactions.urls')),
    path('limits/', include('budget.urls')),
    path('finscope/', include('finscope.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
