from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Tieba, Comment
from .forms import PostForm, LoginForm, RegisterForm

def home(request):
    """首页视图 - 显示帖子列表和热门贴吧"""
    # 获取帖子列表，按置顶和创建时间排序
    posts = Post.objects.filter(status=1).order_by('-is_top', '-created_at')[:20]
    
    # 获取热门贴吧列表
    hot_tiebas = Tieba.objects.filter(status=1).order_by('-member_count')[:10]
    
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
                        owner=User.objects.first() or None,  # 使用第一个用户或None
                        member_count=10000 + i * 1000
                    )
                
                # 创建模拟帖子
                Post.objects.create(
                    title=f'测试帖子标题{i+1}: 这是一个很好的测试主题',
                    content=f'这是第{i+1}个测试帖子的内容。\n\n这里可以包含多行文本，展示帖子的详细内容。\n\n测试数据第{i+1}条。',
                    tieba=tieba,
                    is_top=1 if i < 3 else 0,
                    is_essence=1 if i >=3 and i < 5 else 0,
                    view_count=(i+1)*100,
                    reply_count=(i+1)*5,
                    like_count=(i+1)*20,
                )
            except Exception as e:
                print(f"创建模拟数据失败: {e}")
        
        # 重新获取帖子列表和热门贴吧
        posts = Post.objects.filter(status=1).order_by('-is_top', '-created_at')[:20]
        hot_tiebas = Tieba.objects.filter(status=1).order_by('-member_count')[:10]
    
    return render(request, 'encyclopedia/list.html', {'entries': posts, 'hot_tiebas': hot_tiebas})

def post_detail(request, title):
    """帖子详情视图"""
    try:
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
                return redirect('post_detail', title=default_post.title)
            raise Http404("没有找到可用的帖子")
        except:
            # 如果没有任何帖子，显示一个友好的错误页面
            return render(request, 'encyclopedia/detail.html', {'entry': None})

@login_required(login_url='/login/')
def post_create(request):
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
                    description='这是系统创建的默认贴吧',
                    member_count=100
                )
            post.tieba = tieba
            
            post.save()
            messages.success(request, '帖子发布成功！')
            return redirect('home')
    else:
        form = PostForm()
    
    # 获取所有贴吧列表
    tiebas = Tieba.objects.all()
    return render(request, 'encyclopedia/create.html', {'form': form, 'tiebas': tiebas})

def post_edit(request, title):
    """编辑帖子视图"""
    post = get_object_or_404(Post, title=title, status=1)
    
    # 检查权限
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, '您没有权限编辑此帖子')
        return redirect('post_detail', title=post.title)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '帖子编辑成功！')
            return redirect('post_detail', title=post.title)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'encyclopedia/edit.html', {'form': form, 'entry': post})

def user_login(request):
    """用户登录视图"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, '登录成功！')
                return redirect('home')
            else:
                messages.error(request, '用户名或密码错误')
    else:
        form = LoginForm()
    
    return render(request, 'encyclopedia/login.html', {'form': form})

def user_logout(request):
    """用户登出视图"""
    logout(request)
    messages.success(request, '已成功登出')
    return redirect('home')

def user_register(request):
    """用户注册视图"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # 自动登录
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, '注册成功！欢迎加入百度贴吧')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'encyclopedia/register.html', {'form': form})

def tieba_detail(request, tieba_name):
    """贴吧详情视图"""
    tieba = get_object_or_404(Tieba, name=tieba_name, status=1)
    
    # 获取该贴吧的帖子列表
    posts = Post.objects.filter(tieba=tieba, status=1).order_by('-is_top', '-created_at')[:20]
    
    return render(request, 'encyclopedia/tieba_detail.html', {'tieba': tieba, 'posts': posts})
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