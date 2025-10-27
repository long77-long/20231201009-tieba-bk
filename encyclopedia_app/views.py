from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Post, Tieba, Comment
from .forms import PostForm

def entry_list(request):
    """首页视图 - 显示帖子列表"""
    # 为了兼容原有的URL结构，暂时保持视图名称不变
    # 获取帖子列表，按置顶和创建时间排序
    posts = Post.objects.filter(status=1).order_by('-is_top', '-created_at')[:20]
    
    # 添加一些模拟数据以便展示
    if not posts.exists():
        # 创建一些模拟数据
        for i in range(10):
            # 尝试获取第一个贴吧，如果不存在则创建
            try:
                tieba = Tieba.objects.first()
                if not tieba:
                    tieba = Tieba.objects.create(
                        name='热门话题吧',
                        description='这是一个热门话题讨论吧',
                        owner=None,  # 实际应用中应该设置为真实用户
                    )
                
                # 创建模拟帖子
                Post.objects.create(
                    title=f'测试帖子标题{i+1}: 这是一个很好的测试主题',
                    content=f'这是第{i+1}个测试帖子的内容。\n\n这里可以包含多行文本，展示帖子的详细内容。\n\n测试数据第{i+1}条。',
                    tieba=tieba,
                    is_top=1 if i < 3 else 0,
                    is_essence=1 if i >=3 and i < 5 else 0,
                    view_count=(i+1)*123,
                    reply_count=(i+1)*12,
                    like_count=(i+1)*45,
                )
            except Exception as e:
                print(f"创建模拟数据失败: {e}")
        
        # 重新获取帖子列表
        posts = Post.objects.filter(status=1).order_by('-is_top', '-created_at')[:20]
    
    return render(request, 'encyclopedia/list.html', {'entries': posts})

def entry_detail(request, title):
    """帖子详情视图"""
    try:
        # 为了兼容原有的URL结构，我们尝试通过标题查找帖子
        # 在实际应用中，应该使用ID作为URL参数
        post = Post.objects.get(title=title, status=1)
        # 增加浏览次数
        post.view_count += 1
        post.save()
        
        # 获取评论列表
        comments = Comment.objects.filter(post=post, status=1).order_by('created_at')
        
        return render(request, 'encyclopedia/detail.html', {'entry': post, 'comments': comments})
    except Post.DoesNotExist:
        # 如果找不到帖子，尝试查找第一个帖子作为默认展示
        try:
            default_post = Post.objects.filter(status=1).first()
            if default_post:
                return redirect('entry_detail', title=default_post.title)
            raise Http404("没有找到可用的帖子")
        except:
            # 如果没有任何帖子，显示一个友好的错误页面
            return render(request, 'encyclopedia/detail.html', {'entry': None})

@login_required(login_url='/admin/login/')  # 简化版，实际应该使用自定义登录页面
@login_required(login_url='/admin/login/')
def entry_create(request):
    """创建帖子视图"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # 获取第一个贴吧作为默认贴吧
            tieba = Tieba.objects.first()
            if not tieba:
                tieba = Tieba.objects.create(
                    name='默认贴吧',
                    owner=request.user,
                    description='这是系统创建的默认贴吧'
                )
            post.tieba = tieba
            
            post.save()
            return redirect('entry_list')
    else:
        form = PostForm()
    
    # 获取所有贴吧列表
    tiebas = Tieba.objects.all()
    return render(request, 'encyclopedia/create.html', {'form': form, 'tiebas': tiebas})

def entry_edit(request, title):
    """编辑帖子视图"""
    post = get_object_or_404(Post, title=title, status=1)
    
    # 检查权限（简化版）
    # 实际应用中应该检查用户是否为帖子作者或管理员
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('entry_detail', title=form.cleaned_data['title'])
    else:
        form = PostForm(instance=post)
    
    return render(request, 'encyclopedia/edit.html', {'form': form, 'entry': post})