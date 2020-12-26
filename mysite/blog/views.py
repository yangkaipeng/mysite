from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list,2)   # 每两篇文章分一页
    page = request.GET.get('page')  # 指明页数
    try:
        posts = paginator.page(page)    # 在期望的页面获得对象
    except PageNotAnInteger:
        # 如果page不是个整数，就返回第一页的内容
        posts = paginator.page(1)
    except EmptyPage:
        # 如果超出了最大页数，就显示最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',{'page':page,'posts':posts})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    
    return render(request, 'blog/post/detail.html',{'post':post})



