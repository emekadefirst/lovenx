from django.contrib import admin
from .models import Wallet, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = (
        "amount", "type", "category", "status", "description",
        "reference", "previous_balance", "new_balance",
        "crypto_amount", "crypto_currency", "created_at"
    )
    can_delete = False
    show_change_link = True


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "walled_id", "balance", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "walled_id")
    readonly_fields = ("walled_id", "created_at", "updated_at")
    inlines = [TransactionInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet", "amount", "type", "category", "status",
        "reference", "previous_balance", "new_balance",
        "crypto_amount", "crypto_currency", "created_at"
    )
    list_filter = ("type", "category", "status", "crypto_currency", "created_at")
    search_fields = ("wallet__user__username", "wallet__walled_id", "reference")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
