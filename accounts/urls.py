from django.urls import path
from .views import login_view
from .views import dashboard_view
from . import views


urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'), 
    path('logout/', views.logout_view, name='logout'),

]
