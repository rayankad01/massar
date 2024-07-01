from django.urls import path
from info.views import privacy_policy
app_name = "info"
urlpatterns = [
    path('privacy-policy/', privacy_policy, name="privacy_policy"),

]