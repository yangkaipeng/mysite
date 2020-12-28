from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')  # 在管理界面展示的字段
    list_filter = ('status', 'created', 'publish', 'author')   # 右边筛选栏
    search_fields = ('title','body')  # 搜索框
    prepopulated_fields = {'slug':('title',)}    # 根据title信息自动填充slug
    raw_id_fields = ('author',)    # 将其中字段放入一个搜索控件中
    date_hierarchy = 'publish'    # 根据指定日期字段添加时间导航栏
    ordering = ['status','publish']    # 展示顺序
    list_editable = ['status',]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')