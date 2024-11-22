from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Rating(models.Model):
    image = models.ImageField(upload_to='images/')
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )

    def __str__(self):
        return str(self.pk)


class Review(models.Model):
    image = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.created_at}"

