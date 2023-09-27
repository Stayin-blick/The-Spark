from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from taggit.models import Tag
from .models import Post
from .forms import CommentForm, BlogPostForm, UserProfileForm, EditBlogPostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify


class UserProfile(View):

    def get(self, request):
        # Get the user's profile
        user_profile = request.user.userprofile
        form = UserProfileForm(instance=user_profile)
        return render(request, 'user_profile.html', {'form': form})

    def post(self, request):
        user_profile = request.user.userprofile
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        return render(request, 'user_profile.html', {'form': form})


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_date")
    template_name = "index.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
        return queryset


class Create_Post(View):

    def get(self, request):
        form = BlogPostForm(initial={'author': request.user.username})
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            tags = request.POST.get('tags')
            if tags:
                tag_list = tags.split(',')
                for tag_name in tag_list:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name.strip())
                    post.tags.add(tag)
            return redirect(reverse_lazy('home'))
        else:
            return render(request, 'create_post.html', {'form': form})


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.post_comments.filter(
            approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_details.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked,
                "comment_form": CommentForm,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_details.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )

@method_decorator(login_required, name='dispatch')
class EditPost(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        # Check if the user is the author of the post
        if request.user != post.author:
            # Handle unauthorized access (e.g., show an error message)
            return redirect('post_details', slug=slug)

        # Prepopulate the form with the existing post data
        form = EditBlogPostForm(instance=post)

        return render(request, 'edit_post.html', {'form': form, 'post': post})

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        # Check if the user is the author of the post
        if request.user != post.author:
            # Handle unauthorized access (e.g., show an error message)
            return redirect('post_details', slug=slug)

        form = EditBlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)

            # Update the slug to match the new title (if it has changed)
            new_slug = slugify(post.title)
            if post.slug != new_slug:
                post.slug = new_slug
                post.save()  # Save the post to update the slug in the database

            post.save()

            # Redirect to the updated post details page with the new slug
            return redirect('post_details', slug=post.slug)

        return render(request, 'edit_post.html', {'form': form, 'post': post})


@method_decorator(login_required, name='dispatch')
class DeletePost(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        # Check if the user is the author of the post
        if request.user != post.author:
            # Handle unauthorized access (e.g., show an error message)
            return redirect('post_details', slug=slug)

        # Delete the post
        post.delete()
        return redirect('home')


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user.id)

        return HttpResponseRedirect(reverse('post_details', args=[slug]))
