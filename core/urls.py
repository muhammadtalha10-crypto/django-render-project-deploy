
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    path("fields/", views.lab_index, name="lab_index"),
    path("fields/delete/<str:key>/<int:pk>/", views.lab_delete, name="lab_delete"),
]



