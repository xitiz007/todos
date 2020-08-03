from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name= 'homepage'),
    path('signup/', views.signup_user, name= 'signup'),
    path('currenttodos/', views.current_todos, name= 'current_todos'),
    path('logout/', views.logout_user, name= 'logout'),
    path('login/', views.login_user, name= 'login'),
    path('createtodo/', views.create_todo, name= 'create'),
    path('todo/<int:todo_id>', views.view_todo, name= 'view_todo'),
    path('todo/<int:todo_id>/completed', views.completed_todo, name= 'completed_todo'),
    path('todo/<int:todo_id>/delete', views.delete_todo, name= 'delete_todo'),
    path('completedtodos/', views.completed_todos, name= "completed_todos"),
    path('todo/<int:todo_id>/unfinish', views.unfinish_todo, name= 'unfinish_todo'),
    path('todo/<int:todo_id>/deletecompleted', views.delete_todo_completed, name= 'delete_todo_completed')
]
