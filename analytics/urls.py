from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import analytics, implementation_plan, deviation_analysis, report_RKDZ
from .analytics import get_analytics_for_all_contracts, get_deviation_analysis

app_name = "analytics"


urlpatterns = [
    path('', analytics, name='analytics'),
    path('implementation_plan/', get_analytics_for_all_contracts, name='implementation_plan'),
    path('deviation_analysis/', get_deviation_analysis, name='deviation_analysis'),
    path('report_RKDZ/', report_RKDZ, name='report_RKDZ'),

]
