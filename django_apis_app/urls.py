from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = "login" ),
    path('login', LoginApi.as_view()),
    path('get_data', GetData.as_view()),
    path('home/', test),
    path('home/<int:id>', singleview),
    path('logout/', signout, name = "logout" ),
]