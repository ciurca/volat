from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name='user-page'),
    path('account/', views.accountSettings, name='account-settings'),
    path('event/<int:pk>', views.EventView.as_view(), name="event"),
    path('event/<int:event_id>/generateContract', views.generateContract, name="generateContract"),

]