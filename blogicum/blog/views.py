from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404

from blog.forms import CommentForm, PostForm, ProfileForm
from blog.models import Category, Comment, Post
from blog.utils import posts_pagination, query_post


def index(request):

    page_obj = posts_pagination(request, query_post())
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):

    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    page_obj = posts_pagination(
        request,
        query_post(manager=category.posts)
    )
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if not post.is_published and post.author != request.user:
        raise Http404
    
    comments = post.comments.all().order_by('created_at')
    form = CommentForm()
    return render(request, 'blog/detail.html', {
        'post': post,
        'form': form,
        'comments': comments
    })


@login_required
def create_post(request):

    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def edit_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def profile(request, username):

    profile = get_object_or_404(User, username=username)
    posts = query_post(manager=profile.posts, filters=profile != request.user)
    page_obj = posts_pagination(request, posts)
    context = {'profile': profile,
               'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):

    form = ProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/user.html', context)


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
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form, 'comment': comment}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)
    if request.method == "POST":
        comment.delete()
        return redirect('blog:post_detail', post_id)
    context = {'comment': comment}
    return render(request, 'blog/comment.html', context)
