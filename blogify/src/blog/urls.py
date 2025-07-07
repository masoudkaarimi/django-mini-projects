from django.urls import path, re_path

from blog.views import BlogView

app_name = "blog"

urlpatterns = [
    path('', BlogView.archive_post_list_view, name="archive_post_list"),
    re_path(r'^category/(?P<slug>[^/]+)/?$', BlogView.category_post_list_view, name="category_posts_list"),
    re_path(r'^tag/(?P<slug>[^/]+)/?$', BlogView.tag_post_list_view, name="tag_posts_list"),
    path("author/<str:username>/", BlogView.author_post_list_view, name="author_posts_list"),
    path("search/", BlogView.search_post_list_view, name="search_posts_list"),
    re_path(r"^(?P<slug>[^/]+)/?$", BlogView.post_detail_view, name="post_detail"),
]
