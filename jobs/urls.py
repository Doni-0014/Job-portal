from django.urls import path
from . import views


urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('applications/manage/', views.manage_applications, name='manage_applications'),
    path('recommendations/', views.recommendations, name='recommendations'),
]


