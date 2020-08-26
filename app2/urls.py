from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.signup , name="signup"),
    path('signin/',views.signin , name='signin'),
    path('logout/',views.logout , name='logout'),
    path('success/',views.success , name='success'),


]
