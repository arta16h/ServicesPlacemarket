from django.contrib import admin
from .models import LeaderboardEntry, LeaderboardSettings

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("provider", "rank", "score", "month", "year")
    list_filter = ("month", "year")
    search_fields = ("provider__username",)

@admin.register(LeaderboardSettings)
class LeaderboardSettingsAdmin(admin.ModelAdmin):
    list_display = ("weight_orders", "weight_ratings")

    def has_add_permission(self, request):
        # فقط یه تنظیمات وجود داشته باشه
        if LeaderboardSettings.objects.exists():
            return False
        return True
