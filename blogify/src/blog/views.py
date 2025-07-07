from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.translation import gettext as _

from blog.forms import CommentForm
from blog.models import Category, Post, Tag, Comment
from main.utils import toast


class BlogView(View):
    @classmethod
    def archive_post_list_view(cls, request, *args, **kwargs):
        # ajax search
        authors = get_user_model().objects.filter(is_staff=True)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        posts = Post.objects.filter(status=Post.PostStatusChoices.PUBLISHED)
        latest_posts = posts.order_by('-created_at')[:6]
        # top_posts = Post.objects.all().order_by('-views')[:6]
        # popular_posts = Post.objects.filter(status=Post.PostStatusChoices.PUBLISHED).order_by('-views')[:6]

        context = {
            'title': 'Home',
            'authors': authors,
            'categories': categories,
            'tags': tags,
            'posts': posts,
            'latest_posts': latest_posts,
            # 'top_posts': popular_posts,
            # 'popular_posts': popular_posts,
        }
        return render(request, "main/home.html", context)

    @classmethod
    def category_list_view(cls, request, *args, **kwargs):
        categories = get_object_or_404(Category)

        context = {
            'title': _("Categories"),
            'categories': categories,
        }
        return render(request, "blog/category-list.html", context)

    @classmethod
    def category_post_list_view(cls, request, slug, *args, **kwargs):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        category = get_object_or_404(Category.objects.prefetch_related('category_post'), slug=slug)
        posts = category.category_post.filter(status=Post.PostStatusChoices.PUBLISHED)

        context = {
            'title': _("Category: %(category)s") % {'category': category.name},
            'category': category,
            'categories': categories,
            'tags': tags,
            'posts': posts,
        }
        return render(request, "blog/category-list.html", context)

    @classmethod
    def tag_list_view(cls, request, *args, **kwargs):
        # tags = Tag.objects.all()
        context = {'title': _("Tags")}
        return render(request, "blog/tag-list.html", context)

    @classmethod
    def tag_post_list_view(cls, request, slug, *args, **kwargs):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        tag = get_object_or_404(Tag.objects.prefetch_related("tag_post"), slug=slug)
        posts = tag.tag_post.filter(status=Post.PostStatusChoices.PUBLISHED)

        context = {
            'title': _("Tags"),
            'tag': tag,
            'tags': tags,
            'categories': categories,
            'posts': posts,
        }
        return render(request, "blog/tag-list.html", context)

    @classmethod
    def author_list_view(cls, request, *args, **kwargs):
        # authors = Author.objects.all()
        context = {'title': _("Authors")}
        return render(request, "blog/author-list.html", context)

    @classmethod
    def author_post_list_view(cls, request, username, *args, **kwargs):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        author = get_object_or_404(get_user_model().objects.all(), username=username)

        context = {
            'title': _("Authors"),
            'tags': tags,
            'categories': categories,
            'author': author,
        }
        return render(request, "dashboard/profile.html", context)

    @classmethod
    def search_post_list_view(cls, request, *args, **kwargs):
        categories = Category.objects.all()
        tags = Tag.objects.all()
        posts = Post.objects.filter(status=Post.PostStatusChoices.PUBLISHED)

        context = {
            'title': _("Archives"),
            'tags': tags,
            'categories': categories,
            'posts': posts,
        }
        return render(request, "blog/search-list.html", context)

    @classmethod
    def post_detail_view(cls, request, slug, *args, **kwargs):
        authors = get_user_model().objects.filter(is_staff=True)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        posts = Post.objects.filter(status=Post.PostStatusChoices.PUBLISHED)
        related_posts = posts.order_by('-created_at')[:12]

        post = get_object_or_404(Post, slug=slug)
        comments = Comment.objects.filter(post=post, status=Comment.CommentStatusChoices.APPROVED)


        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                # Todo: Check if status is approved
                post.comments_count += 1
                post.save()
                toast(request, _('Comment added successfully!\nAfter approval, it will be displayed.'), 'success')
                return redirect(post.get_absolute_url())
        else:
            form = CommentForm(initial={'post': post.pk, 'author': request.user.pk})

        context = {
            'title': _("Post Details"),
            'breadcrumb_items': [
                {"title": post.title, "url": ""},
            ],
            "form": form,
            "post": post,
            "posts": posts,
            'authors': authors,
            'categories': categories,
            'tags': tags,
            "related_posts": related_posts,
            "comments": comments,
            "has_comment": post.comment_status == Post.CommentStatusChoices.OPEN,
        }

        return render(request, "blog/post-detail.html", context)
