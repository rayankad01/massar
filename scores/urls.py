from django.urls import path
from scores.views import display_scores, count_score
app_name = "scores"
urlpatterns = [
    path('display/', display_scores, name="display"),
    path('count/', count_score, name="count"),

]