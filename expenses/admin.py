from django.contrib import admin

from .models import Expense, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "amount",
        "date",
        "category",
        "user",
    )
    list_filter = ("category", "date")
    search_fields = ("title", "user__username")
