from django.urls import path

from . import views

urlpatterns = [
    path('',views.loginUser, name=''),
    path('login',views.loginUser, name='login'),
    path('register',views.register_user, name="register"),
    path('home', views.home, name="home"),
    path('logout',views.logoutUser, name="logout"),
    path('help',views.help, name="help"),
    path('history',views.get_history, name="history"),
    path('status_data',views.download_excel_data, name='status_data'),
    path('project_data',views.project_data,name="project_data"),
    path('update_project',views.update_project,name='update_project')
]