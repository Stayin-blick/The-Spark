from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager

STATUS = ((0, "Draft"), (1, "Published"))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('image', default='/blog/images/default_user.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    featured_image = CloudinaryField('image', default='placeholder')
    tags = TaggableManager()
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)
    likes = models.ManyToManyField(
        User, related_name='blogpost_likes', blank=True)
    comments = models.ManyToManyField(
        'Comment', related_name='post_num_comments', blank=True)

    class meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.__class__.objects.filter(slug=self.slug).exists():
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def number_of_likes(self):
        return self.likes.count()

    def number_of_approved_comments(self):
        return self.post_comments.filter(approved=True).count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
