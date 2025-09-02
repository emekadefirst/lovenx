import uuid
import random
from django.db import models
from django.contrib.auth.models import User

def generate_walled_id():
    return str(random.randint(1000000000, 9999999999))


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        abstract = True


class Wallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    walled_id = models.CharField(max_length=10, unique=True, null=True, blank=True)


    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.walled_id:
            self.walled_id = generate_walled_id()
        super().save(*args, **kwargs)


class Transaction(BaseModel):
    class Type(models.TextChoices):
        CREDIT = 'CREDIT', 'Credit'
        DEBIT = 'DEBIT', 'Debit'

    class Category(models.TextChoices):
        WITHDRAWAL = 'WITHDRAWAL', 'Withdrawal'
        DEPOSIT = 'DEPOSIT', 'Deposit'
        SELL = 'SELL', 'Sell'
        BUY = 'BUY', 'Buy'
        REFUND = 'REFUND', 'Refund'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=6, choices=Type.choices)
    category = models.CharField(max_length=10, choices=Category.choices)    
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    description = models.TextField(null=True, blank=True)
    reference = models.CharField(max_length=100, unique=True)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    crypto_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    crypto_currency = models.CharField(max_length=10, null=True, blank=True)    