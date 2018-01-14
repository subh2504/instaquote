from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.
try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404,JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone
from django.urls import reverse

from .forms import PostForm
from .models import Post,Like



def post_create(request):
    form = PostForm(request.POST or None,auto_id=False)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        print(instance.get_absolute_url)
        return HttpResponseRedirect(reverse('quotes:list'))
    context = {
        "form": form,
    }
    return  HttpResponseRedirect(reverse('quotes:list'))


def post_detail(request, pk=None):
    user = request.user
    instance = get_object_or_404(Post, pk=pk)
    share_string = quote_plus(instance.content)
    is_liked=False
    if request.user.is_authenticated:
        if(instance.like_set.filter(user=user).exists()):
            is_liked=True
    # initial_data = {
    #         "content_type": instance.get_content_type,
    #         "object_id": instance.id
    # }
    
    context = {
        "title": "gg",
        "instance": instance,
        "share_string": share_string,
        "is_liked":is_liked
        
    }
    return render(request, "quotes/quote_detail.html", context)


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if obj.like_set.filter(user=user).exists():
            print("Already Liked")
        else:
            l=Like(Post=obj,user=user)
            l.save()
            print("Liked")
        # if user.is_authenticated:
        #     l = Like.objects.get()
        #     if user in obj.likes.all():
        #         obj.likes.remove(user)
        #     else:
        #         obj.likes.add(user)
        return url_


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post.objects.active(), pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        print(user.id)
        if obj.like_set.filter(user=user).exists():
            o=obj.like_set.filter(user=user)
            o[0].delete()
            print("Unliked")
            liked=False
        else:
            l=Like(post=obj,user=user)
            l.save()
            obj.like_set.add(l)
            liked=True
            print("Liked")
        count=obj.like_set.all().count()
        updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "count":count
        }
        return Response(data)


class PostLikedByAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = ()
    
    def get(self, request, pk=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post.objects.active(), pk=pk)
        updated = False
        liked_by=obj.like_set.all()
        count=liked_by.count()
        updated = True
        _liked_by=[]
        print(liked_by)
        for u in liked_by:
            user={}
            user["username"]=u.user.get_username()
            user["url"]=reverse('quotes:list_user',args=[u.user.get_username()])
            user["name"]=u.user.get_full_name()
            print(user)
            _liked_by.append(user)
        data = {
            "updated": updated,
            "liked_by": _liked_by,
            "count":count
        }
        return Response(data)


from django.contrib.auth.decorators import login_required

def post_list(request):
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    # if request.user.is_staff or request.user.is_superuser:
    #     queryset_list = Post.objects.all()
    
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
                
    return_list =[]
    if request.user.is_authenticated:
        
        for qs in queryset_list:
            return_list.append((qs, qs.like_set.filter(user=request.user)))
    else:
        for qs in queryset_list:
            return_list.append((qs, False))
            
    paginator = Paginator(return_list, 5) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    
    form = PostForm(request.POST or None)
    
    context = {
        "object_list": queryset, 
        "title": "InstaQuote",
        "page_request_var": page_request_var,
        "form":form,
    }
    return render(request, "quotes/quote_list.html", context)


def post_list_user(request,username=None):
    user=get_object_or_404(User,username__iexact=username)
    queryset_list = Post.objects.active().filter(user=user) #.order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    
    return_list =[]
    if request.user.is_authenticated:
        
        for qs in queryset_list:
            return_list.append((qs, qs.like_set.filter(user=request.user)))
    else:
        for qs in queryset_list:
            return_list.append((qs, False))
    paginator = Paginator(return_list, 4) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    
        
    context = {
        "object_list": queryset, 
        "title":user.get_full_name,
        "page_request_var": page_request_var,
        
    }
    return render(request, "quotes/quote_user_list.html", context)


def post_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.user.get_full_name,
        "instance": instance,
        "form":form,
    }
    return render(request, "quotes/quote_form.html", context)

@login_required
def post_delete(request, pk=None):
    print(pk)
    print(request.user.is_superuser)
    instance = get_object_or_404(Post, pk=pk)
    user=request.user
    print("*")
    print(str(instance.user == user))
    if not request.user.is_superuser and not instance.user == user:
        raise Http404
    instance.delete()
    data={}
    data["success"]=True
    #messages.success(request, "Successfully deleted")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    
@login_required
def post_deactivate(request, pk=None):
    print(pk)
    print(request.user.is_superuser)
    instance = get_object_or_404(Post, pk=pk)
    user=request.user
    print("*")
    print(request.META)
    print(str(instance.user == user))
    if not request.user.is_staff or not request.user.is_superuser and not instance.user == user:
        raise Http404
    if instance.active:
        instance.active=False
    else:
        instance.active=True
    instance.save()
    
    #messages.success(request, "Successfully deleted")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
        
    

@login_required    
def post_list_my(request):
    user=request.user
    queryset_list = Post.objects.all().filter(user=user) #.order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    return_list =[]
    for qs in queryset_list:
        return_list.append((qs, qs.like_set.filter(user=request.user),qs.active))
    paginator = Paginator(return_list, 5) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    
        
    context = {
        "object_list": queryset, 
        "title":user.get_full_name,
        "page_request_var": page_request_var,
        
    }
    return render(request, "quotes/quote_manage.html", context)
    
    
@login_required    
def post_list_manage(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    user=request.user
    
    queryset_list = Post.objects.all() #.order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    return_list =[]
    for qs in queryset_list:
        return_list.append((qs, qs.like_set.filter(user=request.user),qs.active))
    paginator = Paginator(return_list, 5) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    
        
    context = {
        "object_list": queryset, 
        "title":user.get_full_name,
        "page_request_var": page_request_var,
        
    }
    return render(request, "quotes/quote_manage.html", context)