from .models import Comment, Post, UserProfile
from django import forms
from django.contrib.auth.forms import UserChangeForm


class UserProfileForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags', 'featured_image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
