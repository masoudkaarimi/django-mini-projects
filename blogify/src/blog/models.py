from django.db import models
from django.contrib.auth import get_user_model
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField
from autoslug.settings import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from blog.validators import category_thumbnail_validator, post_thumbnail_validator
from main.utils import generate_upload_path


class Post(models.Model):
    class PostStatusChoices(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PENDING = 'pending', _('Pending Review')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')

    class CommentStatusChoices(models.TextChoices):
        OPEN = 'open', _('Open')
        CLOSED = 'closed', _('Closed')

    def thumbnail_path(instance, filename):
        return generate_upload_path(instance, filename, prefix='uploads/posts')

    author = models.ForeignKey(
        get_user_model(),
        related_name='user_post',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_('Post Author'),
        help_text=_('The user who wrote this post. (Required)')
    )
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_('Post Title'),
        help_text=_('The title of the post. (Required)')
    )
    slug = AutoSlugField(
        max_length=255,
        populate_from='title',
        allow_unicode=True,
        unique=True,
        # editable=True,
        # blank=False,
        # null=False,
        verbose_name=_('Post Slug'),
        help_text=_('A unique slug for the post. (Auto-generated - Editable)')
    )
    content = CKEditor5Field(
        config_name='admin',
        blank=False,
        null=False,
        verbose_name=_('Post Content'),
        help_text=_('The content of the post. (Required)')
    )
    excerpt = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Post Excerpt'),
        help_text=_('A short description of the post. (Optional)')
    )
    thumbnail = models.ImageField(
        upload_to=thumbnail_path,
        default=static('assets/images/placeholders/post-thumbnail.webp'),
        blank=True,
        null=True,
        validators=[post_thumbnail_validator],
        verbose_name=_('Post Thumbnail'),
        help_text=_('The thumbnail of the post. (optional)<br />'
                    'The recommended size is <b>1200x630px</b>.<br />'
                    'The supported formats are <b>{allowed_image_extensions}</b>.<br />'
                    'The maximum file size is <b>{max_size}MB</b>.').format(allowed_image_extensions=', '.join(settings.ALLOWED_IMAGE_EXTENSIONS),
                                                                            max_size=settings.MAX_IMAGE_SIZE / 1024)
    )
    category = models.ForeignKey(
        'Category',
        related_name='category_post',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Post Categories'),
        help_text=_('The categories of the post. (Optional)')
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tag_post',
        blank=True,
        verbose_name=_('Post Tags'),
        help_text=_('The tags of the post. (Optional)')
    )
    status = models.CharField(
        max_length=10,
        choices=PostStatusChoices,
        default=PostStatusChoices.DRAFT,
        blank=False,
        null=False,
        verbose_name=_('Post Status'),
        help_text=_('The status of the post. (Required)')
    )
    comment_status = models.CharField(
        max_length=10,
        choices=CommentStatusChoices,
        default=CommentStatusChoices.OPEN,
        blank=False,
        null=False,
        verbose_name=_('Comment Status'),
        help_text=_('The status of the comments for this post. (Required)')
    )
    comments_count = models.IntegerField(
        default=0,
        editable=False,
        blank=False,
        null=False,
        verbose_name=_('Comment Count'),
        help_text=_('The number of comments for this post. (Auto-generated)')
    )
    publish_at = models.DateTimeField(
        default=timezone.now,
        blank=False,
        null=False,
        verbose_name=_('Publish Date'),
        help_text=_('The date and time when the post will be published. (Required)')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created. (Auto-generated)")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated. (Auto-generated)")
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-publish_at']

    def __str__(self):
        return f"{self.author}: {self.slug}"

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_post_thumbnail(self):
        return self.thumbnail.url if self.thumbnail else static('assets/images/placeholders/post-thumbnail.webp')


class Category(MPTTModel):
    def thumbnail_path(instance, filename):
        return generate_upload_path(instance, filename, prefix='uploads/categories')

    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_('Category Name'),
        help_text=_('The name of the category. (Required)')
    )
    slug = AutoSlugField(
        max_length=255,
        populate_from='name',
        allow_unicode=True,
        unique=True,
        # editable=True,
        # blank=False,
        # null=False,
        verbose_name=_('Category Slug'),
        help_text=_('A unique slug for the category. (Auto-generated - Editable)')
    )
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Parent Category'),
        help_text=_('The parent category of this category. (Optional)')
    )
    thumbnail = models.ImageField(
        upload_to=thumbnail_path,
        default=static('assets/images/placeholders/category-thumbnail.webp'),
        blank=True,
        null=True,
        validators=[category_thumbnail_validator],
        verbose_name=_('Category Thumbnail'),
        help_text=_('The thumbnail of the category. (optional)<br />'
                    'The recommended size is <b>512x512px</b>.<br />'
                    'The supported formats are <b>{allowed_image_extensions}</b>.<br />'
                    'The maximum file size is <b>{max_size}MB</b>.').format(allowed_image_extensions=', '.join(settings.ALLOWED_IMAGE_EXTENSIONS),
                                                                            max_size=settings.MAX_IMAGE_SIZE / 1024)
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Category Description'),
        help_text=_('A short description of the category. (Optional)')
    )
    is_active = models.BooleanField(
        default=True,
        blank=False,
        null=False,
        verbose_name=_('Active'),
        help_text=_('The status of the category. (Required)')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created. (Auto-generated)")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated. (Auto-generated)")
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category_posts_list", kwargs={"slug": self.slug})

    def get_category_thumbnail(self):
        return self.thumbnail.url if self.thumbnail else static('assets/images/placeholders/category-thumbnail.webp')


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_('Tag Name'),
        help_text=_('The name of the tag. (Required)')
    )
    slug = AutoSlugField(
        max_length=255,
        populate_from='name',
        allow_unicode=True,
        unique=True,
        # editable=True,
        # blank=False,
        # null=False,
        verbose_name=_('Tag Slug'),
        help_text=_('A unique slug for the tag. (Auto-generated - Editable)')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Tag Description'),
        help_text=_('A short description of the tag. (Optional)')
    )
    is_active = models.BooleanField(
        default=True,
        blank=False,
        null=False,
        verbose_name=_('Active'),
        help_text=_('The status of the tag. (Required)')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created. (Auto-generated)")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated. (Auto-generated)")
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("blog:tag_posts_list", kwargs={"slug": self.slug})


class Comment(MPTTModel):
    class CommentStatusChoices(models.TextChoices):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')
        SPAM = 'spam', _('Spam')
        ARCHIVED = 'archived', _('Archived')

    post = models.ForeignKey(
        Post,
        related_name='post_comment',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_('Associated Post'),
        help_text=_('The post to which this comment belongs. (Required)')
    )
    author = models.ForeignKey(
        get_user_model(),
        related_name='user_comment',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_('Comment Author'),
        help_text=_('The user who wrote this comment. (Required)')
    )
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Parent Comment'),
        help_text=_('The parent comment of this comment. (Optional)')
    )
    content = CKEditor5Field(
        config_name='comment',
        blank=False,
        null=False,
        verbose_name=_('Comment Content'),
        help_text=_('The content of the comment. (Required)')
    )
    status = models.CharField(
        max_length=8,
        choices=CommentStatusChoices,
        default=CommentStatusChoices.PENDING,
        blank=False,
        null=False,
        verbose_name=_('Comment Status'),
        help_text=_('The status of the comment. (Required)')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created. (Auto-generated)")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated. (Auto-generated)")
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author}: {self.content[:50]} - Post: {self.post.title}"
