from django.db import models
from django.contrib.auth.models import User

class Tieba(models.Model):
    """贴吧模型"""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='贴吧名称'
    )
    description = models.TextField(
        verbose_name='贴吧描述',
        blank=True
    )
    avatar = models.CharField(
        max_length=255,
        verbose_name='贴吧头像',
        blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='创建者'
    )
    category_id = models.IntegerField(
        verbose_name='分类ID',
        blank=True,
        null=True
    )
    member_count = models.IntegerField(
        default=0,
        verbose_name='成员数量'
    )
    post_count = models.IntegerField(
        default=0,
        verbose_name='帖子数量'
    )
    status = models.SmallIntegerField(
        default=1,
        verbose_name='状态'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        verbose_name = '贴吧'
        verbose_name_plural = '贴吧'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Post(models.Model):
    """帖子模型"""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=255,
        verbose_name='帖子标题'
    )
    content = models.TextField(
        verbose_name='帖子内容'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='作者',
        null=True,  # 允许匿名发帖
        blank=True
    )
    tieba = models.ForeignKey(
        Tieba,
        on_delete=models.CASCADE,
        verbose_name='所属贴吧'
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name='浏览次数'
    )
    reply_count = models.IntegerField(
        default=0,
        verbose_name='回复次数'
    )
    like_count = models.IntegerField(
        default=0,
        verbose_name='点赞次数'
    )
    is_top = models.SmallIntegerField(
        default=0,
        verbose_name='是否置顶'
    )
    is_essence = models.SmallIntegerField(
        default=0,
        verbose_name='是否精华'
    )
    status = models.SmallIntegerField(
        default=1,
        verbose_name='状态'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-is_top', '-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    """评论模型"""
    id = models.BigAutoField(primary_key=True)
    content = models.TextField(
        verbose_name='评论内容'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='评论者'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='所属帖子'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='父评论',
        null=True,
        blank=True
    )
    floor_number = models.IntegerField(
        verbose_name='楼层'
    )
    like_count = models.IntegerField(
        default=0,
        verbose_name='点赞次数'
    )
    status = models.SmallIntegerField(
        default=1,
        verbose_name='状态'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'