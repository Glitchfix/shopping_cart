from django.db import models
from .user import User
from datetime import datetime, timedelta

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='PENDING')
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(minutes=10))
    
    def cancel(self):
        if self.order.status != 'PENDING':
            raise ValueError("Cannot cancel payment. Order is not in pending status.")
        self.status = 'CANCELED'
        self.order.status = 'CANCELED'
        self.order.save()
        self.save()

    def pay(self):
        if self.order.status != 'PENDING':
            raise ValueError("Cannot pay for the order. Order is not in pending status.")
        self.status = 'PAID'
        self.order.status = 'PAID'
        self.order.save()
        self.save()

    def __str__(self):
        return f"Payment #{self.id} - User: {self.user.username}, Amount: {self.amount}"