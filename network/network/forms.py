from django import forms
from .models import User, Relationship, Post

class New_Post(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    class Meta:
        model = Post
        fields= [
            "content",
        ]
        labels = {
            "content": "Create post",
        }
        widgets = {
            "content": forms.TextInput(attrs={'placeholder': "What's on your mind?"})
        }