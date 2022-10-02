from django import forms
from .models import Post, Comment, Image

class PostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'style': 'padding: 10px; resize: none;'}), required=False)
    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta:
        model = Post
        fields = [
            'caption',
            # 'images',
        ]

class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta:
        model = Image
        fields = [
            'image',
        ]

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'style': 'padding: 10px; resize: none; margin-right:9px;'}), required=False)
    
    class Meta:
        model = Comment
        fields = [
            'comment',
        ]