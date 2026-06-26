from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cases import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('manufacturer/<int:manufacturer_id>/', views.manufacturer_detail, name='manufacturer_detail'),
    path('unknown/', views.unknown_list, name='unknown_list'),
    path('unknown/create/', views.unknown_create, name='unknown_create'),
    path('unknown/<int:unknown_id>/', views.unknown_detail, name='unknown_detail'),
    path('unknown/<int:unknown_id>/add_message/', views.add_message, name='add_message'),
    path('unknown/<int:unknown_id>/delete/', views.delete_unknown, name='delete_unknown'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)