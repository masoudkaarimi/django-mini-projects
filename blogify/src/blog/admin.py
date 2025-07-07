from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from blog.models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'status', 'created_at', 'updated_at',)
    list_filter = ('status', 'created_at', 'updated_at', 'author',)
    search_fields = ('title', 'body',)
    date_hierarchy = 'created_at'
    ordering = ('status', 'created_at',)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at', 'updated_at',)
    ordering = ('name',)


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('post', 'author', 'status', 'created_at', 'updated_at',)
    list_filter = ('status', 'created_at', 'updated_at',)
    search_fields = ('post', 'author', 'status',)
