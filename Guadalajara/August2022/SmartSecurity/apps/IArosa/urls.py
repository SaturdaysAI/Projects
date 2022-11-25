from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'IArosa'

urlpatterns = [
    path(
        '', 
        views.LandingPageView.as_view(),
        name='index'
    ),
    path(
        'map/<month>/<year>', 
        views.Map1View.as_view(),
        name='map'
    ),
]