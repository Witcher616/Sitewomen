from django import template
from django.db.models import Count
from django.core.cache import cache

import women.views as views
from women.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = cache.get_or_set('cat_lst', Category.objects.annotate(count=Count('posts')).filter(count__gt=0), 30)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    tags = cache.get_or_set('tag_lst', TagPost.objects.annotate(count=Count('tags')).filter(count__gt=0), 30)
    return {'tags': tags}
