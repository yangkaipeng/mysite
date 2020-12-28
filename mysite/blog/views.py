from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings

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
    comments = post.comments.filter(active=True)     # 筛选有用评论
    new_comment = None
    if request.method == 'POST':
        # 一个新的评论被post进来
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 创建一个comment object 但是还不保存到DB中
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',{'post':post,
                                                    'comments':comments,
                                                    'new_comment':new_comment,
                                                    'comment_form':comment_form})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = 'published')
    sent = False
    cd = None
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # --send email
            post_url = request.build_absolute_uri(post.get_absolute_url())  # 获取完整URL，包括http schema和主机名
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, settings.EMAIL_HOST_USER,[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent})



