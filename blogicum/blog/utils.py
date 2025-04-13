from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def posts_pagination(
    request, 
    posts_queryset,
    default_page: int = 1,
    per_page: int = 10
):
    """Пагинация постов с настраиваемыми параметрами."""
    paginator = Paginator(posts_queryset, per_page)
    return paginator.get_page(request.GET.get('page', default_page))


def get_posts_queryset(
    base_queryset=Post.objects.all(),
    apply_filters: bool = True,
    with_comments_count: bool = True,
    use_select_related: bool = True,
    apply_default_ordering: bool = True
):
    """
    Формирование QuerySet для постов с гибкими параметрами:
    - apply_filters: Применение фильтров публикации
    - with_comments_count: Добавление количества комментариев
    - use_select_related: Оптимизация запросов к связанным моделям
    - apply_default_ordering: Сортировка по умолчанию из модели
    """
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
