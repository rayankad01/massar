from django.urls import path
from auths.views import login_user
urlpatterns = [
    path('login/', login_user, name="login"),
]