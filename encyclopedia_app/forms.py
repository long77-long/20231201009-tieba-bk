from django import forms
from django.contrib.auth.models import User
from .models import Post

class PostForm(forms.ModelForm):
    """帖子表单"""
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '请输入帖子标题，5-50字',
                    'maxlength': 255
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 15,
                    'placeholder': '请输入帖子内容...',
                    'style': 'min-height: 200px; resize: vertical;'
                }
            ),
        }
        labels = {
            'title': '标题',
            'content': '内容',
        }
        help_texts = {
            'title': '请输入吸引人的标题，让更多人看到你的帖子',
            'content': '详细描述你想分享的内容，可以包含文字、图片等',
        }
    
    def clean_title(self):
        """验证标题"""
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 5:
            raise forms.ValidationError('标题至少需要5个字符')
        if len(title) > 50:
            raise forms.ValidationError('标题不能超过50个字符')
        return title
    
    def clean_content(self):
        """验证内容"""
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 10:
            raise forms.ValidationError('内容至少需要10个字符')
        if len(content) > 5000:
            raise forms.ValidationError('内容不能超过5000个字符')
        return content

class LoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名'
        })
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        })
    )

class RegisterForm(forms.Form):
    """注册表单"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名（3-20个字符）'
        })
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入邮箱'
        })
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码（至少8个字符）'
        })
    )
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请再次输入密码'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        if len(username) < 3 or len(username) > 20:
            raise forms.ValidationError('用户名长度应在3-20个字符之间')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('密码长度至少为8个字符')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', '两次输入的密码不一致')
        
        return cleaned_data