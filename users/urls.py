from django.urls import path
from users import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    # path('login/', obtain_auth_token, name='login'),
]
