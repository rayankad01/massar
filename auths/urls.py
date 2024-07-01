from django.urls import path
from auths.views import login_user, logout_user
app_name = "auths"
urlpatterns = [
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
]