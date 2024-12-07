from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.home_view, name='home'),
    path('candidate_list/', views.candidate_list, name='candidate_list'),
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
