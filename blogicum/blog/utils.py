from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from blog.models import Post

def posts_pagination(request, queryset, per_page=10):
    return Paginator(queryset, per_page).get_page(request.GET.get('page'))

def get_posts(
    posts=Post.objects.all(),
    apply_filters: bool = True,
    with_comments_count: bool = True,
    use_select_related: bool = True,
):
    if use_select_related:
        posts = posts.select_related('author', 'location', 'category')
    if apply_filters:
        posts = posts.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True
        )
    if with_comments_count:
        posts = posts.annotate(comment_count=Count('comments'))
    return posts
