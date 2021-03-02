from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'    # 帖子页面修改的频率
    priority = 0.9    # 它们在网站中的关联性（最大值是1）

    def items(self):
        return Post.objects.all()
        
    def lastmod(self, obj):   # 接收items()返回的每一个对象并且返回对象的最后修改时间
        return obj.updated


