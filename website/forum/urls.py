from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.topics, name="topics"),
    path('add_topic/', views.add_topic, name="add topic"),
    path('<int:topic_id>/', views.threads),
    path('<int:topic_id>/add_thread/', views.add_thread, name="add thread"),
    re_path(r'([0-9]+)/(?P<thread_id>[0-9]+)/', views.posts, name='posts'),
    path('delete/<str:arg>/', views.delete, name='delete')
]
