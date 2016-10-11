# 1 - Stdlib imports
# 2 - Core Django imports
from django import forms
# 3 - Third Party Imports
from pagedown.widgets import PagedownWidget
# 4 - Imports from local app
from .models import Post

class PostForm(forms.ModelForm):
  content = forms.CharField(widget=PagedownWidget(show_preview=False))
  published = forms.DateField(widget=forms.SelectDateWidget)
  class Meta:
    model = Post
    fields = [
      "title",
      "content",
      "image",
      "draft",
      "published",
      ]
