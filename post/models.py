from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from tinymce.models import HTMLField

COLORS = (
    ('bg-danger', 'Red'),
    ('bg-success', 'Greeen'),
    ('bg-primary', 'Blue'),
    ('bg-warning', 'Yellow'),
    ('bg-secondary', 'Grey')
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(
        choices=COLORS,
        default='Green',
        max_length=30
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("post:category", kwargs={"category_slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100)
    # content = models.TextField()
    content = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField()
    url = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"post_slug": self.url})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class ReplyToComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.BooleanField() #like = True / dislike = False


class ViewCount(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    views = models.BigIntegerField(default=0)


class VistedIPs(models.Model):
    ip = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
