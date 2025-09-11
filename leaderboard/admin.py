from django.contrib import admin
from .models import LeaderboardEntry, LeaderboardSettings

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("provider", "rank", "score", "month", "year")
    list_filter = ("month", "year")
    search_fields = ("provider__username",)


