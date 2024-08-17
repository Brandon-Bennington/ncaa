from django.contrib import admin
from .models import Player, YearlyStats, PositionChange, Award

class YearlyStatsInline(admin.TabularInline):
    model = YearlyStats
    extra = 1

class PositionChangeInline(admin.TabularInline):
    model = PositionChange
    extra = 1

class AwardInline(admin.TabularInline):
    model = Award
    extra = 1

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'current_year', 'current_rating', 'career_result')
    search_fields = ('name', 'position')
    list_filter = ('position', 'current_year', 'career_result')
    inlines = [YearlyStatsInline, PositionChangeInline, AwardInline]

admin.site.register(YearlyStats)
admin.site.register(PositionChange)
admin.site.register(Award)
