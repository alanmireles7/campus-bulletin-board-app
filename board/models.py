from django.db import models

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Study Groups', '📚 Study Groups'),
        ('Events', '🎉 Events'),
        ('Housing', '🏠 Housing'),
        ('Clubs', '⭐ Clubs'),
        ('General', '📌 General'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='General')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
