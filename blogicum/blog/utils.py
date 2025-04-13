from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.utils import timezone

from blog.models import Post


def posts_pagination(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def query_post() -> QuerySet:
    return (
        Post.objects
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
        .select_related('category', 'location', 'author')
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )


def get_posts_queryset(
    base_queryset=Post.objects.all(),
    apply_filters: bool = True,
    with_comments_count: bool = True,
    use_select_related: bool = True,
    apply_default_ordering: bool = True
):
    queryset = base_queryset

    if use_select_related:
        queryset = queryset.select_related('author', 'location', 'category')

    if apply_filters:
        queryset = queryset.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True
        )

    if with_comments_count:
        queryset = queryset.annotate(comment_count=Count('comments'))

    if apply_default_ordering:
        return queryset.order_by(*Post._meta.ordering)

    return queryset
