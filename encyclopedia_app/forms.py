from django import forms
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