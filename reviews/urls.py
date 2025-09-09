from django.urls import path
from .views import CreateReviewView, ProviderReviewsView, LeaderboardView

urlpatterns = [
    path("create/", CreateReviewView.as_view(), name="create-review"),
    path("provider/<int:pk>/", ProviderReviewsView.as_view(), name="provider-reviews"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
