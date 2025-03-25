"""
URL configuration for hardwarecommserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from hardwarecommserver import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('hardware/approval', views.treatment_approval),
    path('hardware/status', views.treatment_approval_status),
    path('hardware/remove', views.remove_treatment_approval),
    path('hardware/get_sensor_data_updates', views.get_sensor_data_updates),
    path('hardware/set_sensor_data_updates', views.set_sensor_data_updates),
    path('hardware/get_treatment_progress', views.get_treatment_progress),
    path('hardware/set_treatment_progress', views.set_treatment_progress),
    path('hardware/set_treatment_pause', views.set_treatment_pause),
    path('hardware/get_treatment_pause', views.get_treatment_pause),
    path('hardware/remove_sensor_data', views.remove_sensor_data),
    path('hardware/remove_treatment_progress', views.remove_treatment_progress),
    path('hardware/remove_treatment_pause', views.remove_treatment_pause)
]
