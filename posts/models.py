from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.timezone import now

from users.models import CustomUser



class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    post_picture = models.ImageField(default='default_post.png')
    created_at = models.DateTimeField(default=timezone.now)
    views_count = models.IntegerField(default=0)
    last_viewed_at = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def increment_views(self):
        self.views_count += 1
        self.last_viewed_at = now()
        self.save()

    def __str__(self):
        return self.title



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class PostAuthor(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} by {self.author.first_name} {self.author.last_name}"

class PostReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.stars_given} stars by {self.user.username}"


