"""agaveros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views import View
from agaveros_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('registro',views.registro,name="registro"),
    path('login',views.iniciar_session,name="login"),
    path('exit',views.exit_user, name="exit"),
    path('verificar',views.verificado,name="verificar"),
    path('confirmar',views.confirmar,name="confirmar"),
    path('index_login',views.index_login,name="index_login")
]
