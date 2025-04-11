from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('update/', views.update, name='update'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/add_interests', views.add_interests, name='add_interests'),
    path('profile/find_company/<str:company_name>/', views.find_company, name='find_company'),
    path('profile/<int:interest_pk>', views.delete_interests, name='delete_interests'),
]
