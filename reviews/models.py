from django.db import models

class Review(models.Model):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    provider = models.ForeignKey('users.ProviderProfile', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} - {self.provider.user.username} : {self.rating}"
