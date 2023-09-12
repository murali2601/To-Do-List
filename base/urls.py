from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.home,name="home"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.register,name="register"),
    path('todo/<int:id>/',views.todo,name="todo"),
    path('update/<str:pk>/',views.update,name="update"),
    path('delete/<str:pk>/',views.delete,name="delete"),
]