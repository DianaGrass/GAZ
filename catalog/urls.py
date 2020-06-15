from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.index),
    path('01', views.catalog_funding),
    path('02', views.catalog_activityform),
    path('03', views.catalog_curator),
    path('04', views.catalog_contracttype),
    path('05', views.catalog_contractmode),
    path('06', views.catalog_purchasetype),
    path('07', views.catalog_stateasez),
    path('08', views.catalog_counterpart),
    path('09', views.catalog_contractstatus),
    path('10', views.catalog_usertypes),
    path('11', views.catalog_numberpztru),
    path('12', views.catalog_currency),
    path('13', views.catalog_report),
]
