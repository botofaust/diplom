from django.contrib import admin
from django.urls import path, include

from main.rest_api import router
from main.views import login_api, logout_api, user_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', login_api, name='login'),
    path('api/logout/', logout_api, name='logout'),
    path('api/user_info', user_info, name='user_info'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
