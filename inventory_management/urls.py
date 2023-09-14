from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('inventory/', include('inventory.urls')),
    path('select2/', include('django_select2.urls')),
    
]
