from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy", "service": "Identity Service (Django)"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
]