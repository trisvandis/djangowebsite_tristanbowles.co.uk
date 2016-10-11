from django.shortcuts import render, redirect

from .forms import ContactForm, JoinForm, EmailForm #, JoinForm
from .models import Join

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context


def home_page(request):
  context = {
    'nbar':'home'
    }
  return render(request, 'home.html', context)


def about_page(request):
  context = {
    'nbar':'about'
    }
  return render(request, 'about.html', context)



def contact_form(request):
  form_class = ContactForm
  
  if request.method == 'POST':
    form = form_class(data=request.POST)
    
    if form.is_valid():
      first_name = request.POST.get('first_name', '')
      last_name = request.POST.get('last_name', '')
      email = request.POST.get('email', '')
      subject = request.POST.get('subject', '')
      message = request.POST.get('message', '')
      
      
      template = get_template('contact_template.txt')
      
      context = {
        'first_name': first_name,
        'last_name':last_name,
        'email':email,
        'subject':subject,
        'message':message,
      }
      content = template.render(context)
      
      email = EmailMessage(
          "New contact form submission",
          content,
          "www.tristanbowles.co.uk" + '',
          ['tristanbowles@googlemail.com'],
          headers = {'Reply-To': email }
      )
      email.send()
      return redirect('contact:cthanks')


  return render(request, "contact_form.html", {'form': form_class, 'nbar':'contact'})

def contact_thanks(request):
  return render(request, "contact_thanks.html", {'nbar':'contact'})


def contact_join(request):
  
  form = JoinForm(request.POST or None)
  if form.is_valid():
    new_join = form.save(commit=False)
    email = form.cleaned_data['email']
    new_join, created = Join.objects.get_or_create(email=email) #stops duplicate emails being inputted
   # new_join.save() #use this to save if you didnt want to stop duplicates
    return redirect('contact:thanks')
  context = {
    "form": form,
    "nbar": "subscribe"
    }
  return render(request, "join_form.html", context)
  
  
def contact_jointhanks(request):
  context = {
    "nbar": "subscribe"
    }
  return render(request, "join_thanks.html", context)

def contact_unsubscribe(request):
  
#TODO - Add unsubscribe user from mailing list

  context = {
    "nbar": "subscribe"
    }
  return render(request, "join_unsubscribe.html", context)