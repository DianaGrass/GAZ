from django.contrib import admin
from django.urls import path, include
from planes.views import login_view, logout_view

from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', Schema.as_view()),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('plane/', include('planes.urls', namespace='planes')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('analytics/', include('analytics.urls', namespace='analytics')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]
