from django.forms import ModelForm
from .models import User, Relationship, Post

class New_Post(ModelForm):
    class Meta:
        model = Post
        fields= [
            "content",
        ]
        labels = {
            "content": ("Post:"),
        }
