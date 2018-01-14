from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
        ]
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={'onkeyup':'new do_resize(this)' ,'rows':'1','placeholder': 'Share your quotes', 'class': 'textarea_q form-control'})
            
        }
            