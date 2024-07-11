
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hospital/api/', include('hospitalauth.urls')),
]
