try:
  from urllib.parse import quote_plus
except:
  pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    if not request.user.is_authenticated():
        raise Http404
    
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print (form.cleaned_data.get("title"))
        instance.save()
        #message success
        messages.success(request, "Success: blog entry created!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Unable to create blog entry!")

    context = {
        "form": form,
        "nbar": "blog"
        }
    return render(request, "post_form.html", context)
  
def post_detail(request,slug=None):
    today = timezone.now().date()
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.published > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
      
        new_comment, created = Comment.objects.get_or_create(
                                user = request.user,
                                content_type = content_type,
                                object_id = obj_id,
                                content = content_data,
                                parent = parent_obj,
                                )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    
    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
        "today": today,
        "nbar": "blog"
        }
    return render(request, "post_detail.html", context)

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active().order_by("-timestamp") # order_by("-timestamp") #order by most recently created first
    if request.user.is_staff or request.user.is_superuser: #for staff, so they can see drafts
        queryset_list = Post.objects.all().order_by("-timestamp")
  
    #query deals with search function of blog posts. Links with search input in menu bar
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
              ).distinct() #distinct makes sure no duplciate search items
    
    paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
  
    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var":page_request_var,
        "today": today,
        "nbar": "blog"
        }
    return render(request, "post_list.html", context)

def post_update(request, slug="None"):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print (form.cleaned_data.get("title"))
        instance.save()
        #message success
        messages.success(request, "Success: blog entry updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form" : form,
        "nbar": "blog"
        }
    return render(request, "post_form.html", context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Success: blog entry deleted!")
    return redirect("posts:list")
