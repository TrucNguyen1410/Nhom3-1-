from django.urls import path
from .views import UserAPI, add_user_page, get_users, UserDetailAPI  # Thêm UserDetailAPI vào đây

urlpatterns = [
    path('get-users/', get_users, name='users-list'),
    path('users/<str:email>/', UserDetailAPI.as_view(), name='user-detail'),
    path('users/', UserAPI.as_view(), name='user-api'),
    path('add-user/', add_user_page, name='add-user-page'),
]
