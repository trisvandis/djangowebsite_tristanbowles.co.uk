#### Imports ####
# 1 - Stdlib imports
# 2 - Core Django imports
from django import forms
#3  - Third Party Imports
#4  - Imports from local apps
#### end of imports ####

class CommentForm(forms.Form):
  content_type = forms.CharField(widget=forms.HiddenInput)
  object_id = forms.IntegerField(widget=forms.HiddenInput)
  #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
  content = forms.CharField(label='', widget=forms.Textarea)
  