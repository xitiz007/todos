from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns= [
    path('', views.home_page, name= 'homepage'),
    path('signup/', views.sign_up_user, name= 'signup'),
    path('currenttodos/', views.current_todos, name= 'current_todos'),
    path('logout/', views.logout_user, name= 'logout'),
    path('login/', views.sign_in_user, name= 'login'),
    path('createtodo/', views.create_todo, name= 'create'),
    path('todo/<int:todo_id>', views.view_todo, name= 'view_todo'),
    path('todo/<int:todo_id>/completed', views.completed_todo, name= 'completed_todo'),
    path('todo/<int:todo_id>/delete', views.delete_todo, name= 'delete_todo'),
    path('completedtodos/', views.completed_todos, name= "completed_todos"),
    path('todo/<int:todo_id>/unfinish', views.unfinish_todo, name= 'unfinish_todo'),
    path('todo/<int:todo_id>/deletecompleted', views.delete_todo_completed, name= 'delete_todo_completed'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name= 'todo/reset.html'), name= 'password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name= 'todo/reset_done.html'), name= 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'todo/reset_confirm.html'), name= 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name= 'todo/reset_complete.html'), name= 'password_reset_complete'),

    path('profile/', views.profile, name= 'profile'),
    path('change_password', views.change_password, name= 'change_password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
