from django.urls import path , include
from .views import *
urlpatterns = [
    
    path('login/' , login_view , name='login'),
    path('logout/' , logout_view , name='logout'),
    path('signup/' , signup_view , name='signup'),
    path('profile/' , profile , name='profile'),
    path('change_password/' , change_password , name='change_password'),
    path('change_email/' , change_email , name='change_email'),
    path('delete_user/' , delete_user , name='delete_user'),
    path('add_address/' , add_address , name='add_address'),
    path('edit_address/<int:id>/' , edit_address , name='edit_address'),
    path('delete_address/<int:id>/' , delete_address , name='delete_address'),
    path('verify/<auth_token>/' , verify_mail , name='verify'),
    
    # admin actions
    path('manage_users/' , AdminActions.manage_users , name='manage_users'),
    path('view_user/<int:id>/' , AdminActions.view_user , name='view_user'),
    path('user_delete/<int:id>/' , AdminActions.delete_user_by_admin , name='delete_user_by_admin'),
]
