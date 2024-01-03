from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile,Post,LikePost,Followers
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):
  try:
    if request.method == 'POST':
      fnm = request.POST.get('fnm')
      emailid = request.POST.get('emailid')
      pwd = request.POST.get('pwd')
      my_user = User.objects.create_user(fnm,emailid,pwd)
      my_user.save()
      user_model = User.objects.get(username = fnm)
      new_profile = Profile.objects.create(user = user_model,id_user=user_model.id)
      new_profile.save()
      if my_user is not None:
        login(request,my_user)
        return redirect('/')
      return redirect('/login')
  except:
    invalid = 'user already exists'
    return render (request,'signup.html',{'invalid':invalid})
  return render (request,'signup.html')
  

def login (request):
  if request.method == 'POST':
    fnm = request.POST.get('fnm')
    pwd = request.POST.get('pwd')
    print(fnm,pwd)
    userr = authenticate(request,username = fnm,password = pwd)
    if userr is not None:
      login(request,userr)
      return redirect('/')
    invalid = 'invalid credentials'
    return render(request,'loginn.html',{'invalid':invalid})
  return render(request,'loginn.html')




@login_required(login_url='/login')
def logout(request):
  logout(request)
  return redirect ('login/')


@login_required(login_url='/login')
def upload(request):
  if request.method == 'POST':
    user = request.user.username
    image = request.FILES.get('image-upload')
    caption = request.POST['caption']
    new_post = Post.objects.create(user=user,image=image,caption=caption)
    new_post.save()
    return redirect('/')
  else:
    return redirect('/')
  
  
@login_required(login_url='/login')
def home (request):
  following_users = Followers.objects.filter(follower=request.user.username).values_list('user',flat=True)
  post = Post.objects.filter(Q(user=request.user.username)| Q(user__in=following_users)).order_by('created_at')
  profile = Profile.objects.get(user = request.user)
  context = {
    'post':post,
    'profile':profile,
  }
  return render (request,'main.html',context)


@login_required(login_url='/login')
def likes(request,id):
  if request.method == 'GET':
    username=request.user.username
    post = get_object_or_404(Post,id=id)
    like_filter = LikePost.objects.filter(post_id=id,username=username).first()
    if like_filter is None:
      new_like = LikePost.objects.create(post_id=id,username=username)
      post.no_of_likes += 1
      
    else:
      like_filter.delete()
      post.no_of_likes -=  1
      
  post.save()
  return redirect('/')

@login_required(login_url='/login')
def home_posts(request,id):
  post = Post.objects.get(id=id)
  profile = Profile.objects.get(user=request.user)
  context = {
    'profile':profile,
    'post':post,
  }

  return render (request,'main.html',context)

@login_required(login_url='/login')
def explore (request):
  post = Post.objects.all().order_by('created_at')
  # profile = Profile.objects.get(user=request.user)
  context={
    'post':post,
    # 'profile':profile,

  }
  return render(request,'explore.html',context)



@login_required(login_url='/login')
def profile(request,id_user):

  user_object = User.objects.get(username=id_user)
  profile = Profile.objects.get(user=request.user)
  user_profile = Profile.objects.get(user=user_object)
  user_posts = Post.objects.filter(user=id_user).order_by('created_at')
  user_post_length = len(user_posts)

  follower = request.user.username
  user = id_user
  if Followers.objects.filter(user=user,follower=follower):
    follow_unfollow = 'UnFollow'
  else:
    follow_unfollow = 'Follow'
  
  user_followers = len(Followers.objects.filter(user=id_user))
  user_following = len(Followers.objects.filter(follower = id_user))


  context={
    'user_object':user_object,
    'profile':profile,
    'user_profile':user_profile,
    'user_posts':user_posts,
    'user_post_length':user_post_length,
    'user_followers':user_followers,
    'user_following':user_following,
    'follow_unfollow':follow_unfollow,
  }

  if request.user.username == id_user:

    if request.method == 'POST':

      if request.FILES.get('image')== None:
        image = user_profile.profileimg
        bio = request.POST['bio']
        location = request.POST['location']
        user_profile.image=image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

      if request.FILES.get('image')!= None:
        image = request.FILES.get('image')
        bio = request.POST['bio']
        location = request.POST['location']
        user_profile.image=image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
      return redirect ('/profile/'+id_user)
    
    else:
      return render (request,'profile.html',context)
    

  return render(request,'profile.html',context)


@login_required(login_url='/login')
def follow(request):
  if request.method == 'POST':
    follower = request.POST['follower']
    user = request.POST['user']
    if Followers.objects.filter(follower = follower,user=user).first():
      delete_follower = Followers.objects.get(user=user,follower=follower)
      delete_follower.delete()
      return redirect('/profile/'+user)
    
    else:
      new_follower = Followers.objects.create(user=user,follow=follower)
      new_follower.save()
      return redirect ('/profile/'+user)
  else:
    return redirect ('/')
  


@login_required(login_url='/login')
def delete(request,id):
  post = Post.objects.get(id=id)
  post.delete()
  return redirect('/profile/' + request.user.username)


@login_required(login_url='/login')
def search_results(request):
  query=request.GET.get('q')
  users=Profile.objects.filter(user__username__icontains=query)
  posts=Post.objects.filter(caption__icontains=query)
  context = {
    'query':query,
    'users':users,
    'posts':posts,
  }
  return render(request,'search_user.html',context)





