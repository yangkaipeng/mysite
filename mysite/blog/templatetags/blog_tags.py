from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

# 展示文章总数
@register.simple_tag     # 普通标签
def total_posts():
    return Post.objects.count()

# 展示最新的几篇文章
@register.inclusion_tag('blog/post/latest_posts.html')      # 包含标签
def show_latest_posts(count=3):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}


# 展示评论最多的几篇文章
@register.simple_tag                   # 个人理解的和inclusion的一样，只是看html部分是否单独拿出来
def get_most_commented_posts(count=5):
    return Post.objects.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]