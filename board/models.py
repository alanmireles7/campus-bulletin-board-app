from django.db import models
from django.contrib.auth.models import User

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} on {self.post}"


class Reaction(models.Model):
    EMOJI_CHOICES = [
        ('👍', 'Like'),
        ('❤️', 'Love'),
        ('😂', 'Haha'),
        ('😮', 'Wow'),
        ('😢', 'Sad'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, choices=EMOJI_CHOICES)

    class Meta:
        unique_together = ('post', 'author', 'emoji')

    def __str__(self):
        return f"{self.author} reacted {self.emoji} on {self.post}"