from django.urls import path
from scores.views import display_scores
app_name = "scores"
urlpatterns = [
    path('display/', display_scores, name="display"),
]