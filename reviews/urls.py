from django.urls import path
from .views import CreateReviewView, ProviderReviewsView, LeaderboardView
import logging
logger = logging.getLogger(__name__)


urlpatterns = [
    path("create/", CreateReviewView.as_view(), name="create-review"),
    path("provider/<int:pk>/", ProviderReviewsView.as_view(), name="provider-reviews"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
