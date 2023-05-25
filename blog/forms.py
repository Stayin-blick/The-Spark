from .models import Comment, Post
from django import forms


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags', 'featured_image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
