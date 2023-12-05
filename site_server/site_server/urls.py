
from django.contrib import admin
from django.urls import path, include
# import comp_vision.views as mw
from comp_vision import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls', namespace='users')),
    path('', include('comp_vision.urls', namespace='comp_vision')),
    path('', views.processing, name='processing')
]
