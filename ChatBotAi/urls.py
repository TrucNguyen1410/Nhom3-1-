from turtle import home
from django.contrib import admin
from django.urls import include, path
from users.views import add_user_page
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to ChatBot AI!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('users.urls')),
    path('add-user/', add_user_page, name='add-user-page'),
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),
    path("", home),

]
