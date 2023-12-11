from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .forms import BlogPostForm, CommentForm

class YourAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            status=1,
        )

    def test_post_detail_view(self):
        url = reverse('post_details', args=[self.post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'post_details.html')

    def test_blog_post_form(self):
        form_data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'tags': 'tag1, tag2',
        }
        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form(self):
        form_data = {'body': 'Test Comment'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            status=1,
        )
        self.assertEqual(str(post), 'Test Post')
