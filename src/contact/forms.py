from django import forms
from .models import Join


class ContactForm(forms.Form):
  first_name = forms.CharField(required=True)
  last_name = forms.CharField(required=True)
  email = forms.EmailField(required=True)
  subject = forms.CharField(required=True)
  message = forms.CharField(required=True, widget=forms.Textarea)
  
#  def __init__(self, *args, **kwargs):
#    super(ContactForm, self).__init__(*args, **kwargs)
#    self.fields['first_name'].label = "Your first name:"
#    self.fields['last_name'].label = "Your last name:"
#    self.fields['email'].label = "Your email:"
#    self.fields['subject'].label = "Your subject:"
#    self.fields['message'].label = "Your message:"
  
  

class EmailForm(forms.Form): #regular django form method
  #name = forms.CharField(required=False)
  email = forms.EmailField()
  
  
class JoinForm(forms.ModelForm): #model form method
  class Meta:
    model = Join
    fields = '__all__'