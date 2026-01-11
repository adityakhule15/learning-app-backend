from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/lessons/', include('lessons.urls')),
    path('api/progress/', include('progress_tracker.urls')),
    path('api/admin/', include('admin_api.urls')),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

