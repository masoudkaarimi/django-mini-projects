import os
import random
from faker import Faker
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from blog.models import Post, Category, Tag, Comment

fake = Faker()


def create_categories(n):
    print('Creating categories...')
    categories = []
    for _ in range(n):
        try:
            with transaction.atomic():
                category = Category.objects.create(
                    name=fake.word().capitalize(),
                    description=fake.text(max_nb_chars=100)
                )
                categories.append(category)
                print(f'Category {category.name} created.')
        except IntegrityError:
            print('Failed to create a category due to IntegrityError.')
    return categories


def create_tags(n):
    print('Creating tags...')
    tags = []
    for _ in range(n):
        try:
            with transaction.atomic():
                tag = Tag.objects.create(
                    name=fake.word().capitalize(),
                    description=fake.text(max_nb_chars=100)
                )
                tags.append(tag)
                print(f'Tag {tag.name} created.')
        except IntegrityError:
            print('Failed to create a tag due to IntegrityError.')
    return tags


def create_posts(n, users, categories, tags):
    print('Creating posts...')
    for _ in range(n):
        try:
            with transaction.atomic():
                post = Post.objects.create(
                    author=random.choice(users),
                    title=fake.sentence(),
                    content=fake.text(max_nb_chars=500),
                    excerpt=fake.text(max_nb_chars=200),
                    category=random.choice(categories),
                    status=random.choice([choice[0] for choice in Post.PostStatusChoices.choices]),
                    comment_status=random.choice([choice[0] for choice in Post.CommentStatusChoices.choices]),
                    publish_at=fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
                )
                post.tags.set(random.sample(tags, k=random.randint(1, len(tags))))
                post.save()
                print(f'Post "{post.title}" created.')
        except IntegrityError:
            print('Failed to create a post due to IntegrityError.')


def create_comments(n, users, posts):
    print('Creating comments...')
    for _ in range(n):
        try:
            with transaction.atomic():
                comment = Comment.objects.create(
                    post=random.choice(posts),
                    author=random.choice(users),
                    content=fake.text(max_nb_chars=200),
                    status=random.choice([choice[0] for choice in Comment.CommentStatusChoices.choices])
                )
                print(f'Comment by {comment.author} created.')
        except IntegrityError:
            print('Failed to create a comment due to IntegrityError.')


if os.environ.get('DJANGO_DEBUG'):
    print('Running in development environment...')
    users = list(get_user_model().objects.all())
    if not users:
        print('No user found. Please create some users first.')
    else:
        categories = create_categories(10)
        tags = create_tags(20)
        create_posts(50, users, categories, tags)
        posts = Post.objects.all()
        create_comments(100, users, posts)
        print('Fake data created successfully.')
else:
    print('This script is not allowed to run in the current environment.')
