from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager

# Choices for the 'status' field in the Post model
STATUS = ((0, "Draft"), (1, "Published"))

# UserProfile model representing user profile information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile_picture = CloudinaryField('image', default='/blog/images/default_user.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    # Signal to create a user profile when a new user is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    # Signal to save the user profile when the associated user is saved
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

# Post model representing blog posts
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    featured_image = CloudinaryField('image', default='placeholder')
    tags = TaggableManager()
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)
    likes = models.ManyToManyField(User, related_name='blogpost_likes', blank=True)
    comments = models.ManyToManyField('Comment', related_name='post_num_comments', blank=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title

    # Override the save method to generate a unique slug
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

    # Method to calculate the number of likes for a post
    def number_of_likes(self):
        return self.likes.count()

    # Method to calculate the number of approved comments for a post
    def number_of_approved_comments(self):
        return self.post_comments.filter(approved=True).count()

# Comment model representing comments on blog posts
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
