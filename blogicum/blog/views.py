from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404

from blog.forms import CommentForm, PostForm, ProfileForm
from blog.models import Category, Comment, Post
from blog.utils import posts_pagination, query_post


def index(request):
    return render(
        request,
        'blog/index.html',
        {'page_obj': posts_pagination(request, query_post())}
    )


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'page_obj': posts_pagination(
                request,
                query_post().filter(category=category)
            )
        }
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if not post.is_published:
        if request.user != post.author:
            raise Http404

    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'form': CommentForm(),
            'comments': post.comments.filter(
                is_published=True
            ).order_by('created_at')
        }
    )


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'blog/create.html', {'form': form})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('blog:profile', username=request.user.username)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)

    form = PostForm(
        request.POST or None,
        instance=post,
        files=request.FILES or None
    )
    if not form.is_valid():
        return render(request, 'blog/create.html', {'form': form})

    form.save()
    return redirect('blog:post_detail', post_id)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    return render(
        request,
        'blog/create.html',
        {'form': PostForm(instance=post)}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    queryset = author.posts.order.by('-pub_date')

    if request.user != author:
        queryset = queryset.filter(is_published=True)

    return render(
        request,
        'blog/profile.html',
        {
            'profile': author,
            'page_obj': posts_pagination(request, queryset)
        }
    )


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if not form.is_valid():
        return render(request, 'blog/user.html', {'form': form})

    form.save()
    return redirect('blog:profile', request.user.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect('blog:post_detail', post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    form = CommentForm(request.POST or None, instance=comment)
    if not form.is_valid():
        return render(
            request,
            'blog/comment.html',
            {'form': form, 'comment': comment}
        )

    form.save()
    return redirect('blog:post_detail', post_id)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)

    return render(
        request,
        'blog/comment.html',
        {'comment': comment}
    )
