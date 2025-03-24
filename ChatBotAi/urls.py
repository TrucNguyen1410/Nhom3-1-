from django.contrib import admin
from django.urls import include, path
from users.views import add_user_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('users.urls')),
    path('add-user/', add_user_page, name='add-user-page'),
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),

]
