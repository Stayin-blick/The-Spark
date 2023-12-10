from .models import Comment, Post, UserProfile
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import User

class UserProfileForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['bio'].widget = forms.Textarea(attrs={'rows': 3})


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags', 'featured_image')


class EditBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags', 'featured_image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class CustomSignupForm(SignupForm):

    signup_username = forms.CharField(
        label="signup_username",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a unique username'}),
    )

    #  password fields with verification requirements
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
