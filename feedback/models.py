from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from orders.models import Order
from django.db.models import Avg


class Feedback(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="feedbacks", help_text="Order that the feedback is related to.")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="feedback_given", help_text="User providing the feedback.")
    reviewed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="feedback_received", help_text="User that the feedback is about.")
    comment = models.TextField(help_text="Comments about the order or user.")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rating from 1 (worst) to 5 (best).")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the feedback was created.")

    def __str__(self):
        return f"Feedback for Order {self.order.order_name} - {self.created_at}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        reviewed_user = self.reviewed
        avg_rating = Feedback.objects.filter(reviewed=reviewed_user).aggregate(Avg("rating"))["rating__avg"]
        reviewed_user.rating = avg_rating or 5
        reviewed_user.save()
