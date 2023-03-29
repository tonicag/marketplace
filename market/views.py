from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from .models import Post, Order
from datetime import datetime
from django.db.models.query import QuerySet
def homepage_view(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request=request,template_name='home.html', context=context)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['date_created', 'influencer_id']

@login_required
def create_post(request):
    form = PostForm
    if request.user.is_influencer:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.date_created = datetime.now()
                post.influencer_id = request.user
                post.save()
                form.save_m2m()
                return HttpResponseRedirect('/')
            else:
                messages.error(request,message='Somtehing went wrong!')    
                print("ERROR")
    else:
        return HttpResponseRedirect('/')
    context = {
        'form' : form
    }
    return render(request=request,template_name="market/new_post.html", context=context)

def view_post(request,id):
    try:
        post = Post.objects.get(post_id=id)
    except Post.DoesNotExist:
        post=None
    if post is not None:
        return render(request=request,template_name="market/post.html", context={'post' : post})
    else:
        return reddirect_message(request, "This post doesn't exist")

@login_required
def edit_post(request,id):
    try:
        post = Post.objects.get(post_id=id)
    except Post.DoesNotExist:
        post = None
    if post is None or post.influencer_id.email != request.user.email :
        messages.error(request=request,message='You can''t edit this!')
        return reddirect_message(request, "You can''t edit this!!")
    else:
        form = PostForm(instance=post)
        if request.method=='POST':
            form=PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                print('saved!')
                return reddirect_message(request, "Saving was succesful!")
            else: 
                messages.error(request,message='Something went wrong')
                return reddirect_message(request, "Form is not valid!")
        
        context = {
            'form' : form
        }
        return render(request=request,template_name="market/edit_post.html",context=context)


#Orders

@login_required
def order_post(request,id):
    try:
        post = Post.objects.get(post_id=id)
        
    except Post.DoesNotExist:
        post = None

    try:
        order = Order.objects.get(post_id=id)
    except Order.DoesNotExist:
        order = None
    if order is not None and order.post_id.influencer_id == request.user:
        return reddirect_message(request, "You have already ordered this!")
    if post is None or request.user.is_influencer == True:
        return reddirect_message(request, "You don't have access!")
    if request.method == 'POST':
        order = Order(customer_id=request.user, post_id=post, created_at=datetime.now())
        order.save()
        return reddirect_message(request, "Succes!")
    else:
        context = {
            'post' : post
        }
        return render(request=request,template_name="market/new_order.html",context=context)

@login_required
def view_orders(request):
    if request.user.is_influencer:
        posts = Post.objects.filter(influencer_id=request.user)
        orders = Order.objects.filter(post_id__in=posts)
    else:
        orders = Order.objects.filter(customer_id=request.user)
    
    context = {
        'orders' : orders,
        'count' : orders.count()
    }
    return render(request=request,template_name="market/view_all_orders.html",context=context)



def reddirect_message(request,message):
    context = {
        'message' : message
    }
    return render(request=request,template_name="messages.html", context=context)