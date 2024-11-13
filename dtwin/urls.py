   
from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('dashboard', views.dashboard),
    path('model', views.model),
    path('model.html', views.model),
    path('first_floor.html', views.first_floor),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),

#    path('logout', views.logout),
#    path('logout/', views.logout),
#    path('', include('django.contrib.auth.urls')),
#    path('', include('social_django.urls')),
]
