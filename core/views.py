from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment
from .forms import CommentForm, EditForm, PrefForm
import random
from django.views.generic import UpdateView
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import csv
from django.urls import reverse
# Create your views here.


@login_required(login_url='signin')
def index(request):
    user_object = request.user

    try:
        user_profile = Profile.objects.get(user=user_object)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(
            user=user_object)
        return redirect('settings')


    user_following = user_profile.following.all()

    feed = Post.objects.filter(user__in=user_following).order_by('-created_at')
    
    recommend = []
    for user in user_following:
        following_following = user.following.all()
        for userg in following_following:
            if userg.user not in user_following:  #prob false still continuing  & add suggestion for less than 5 people
                if userg not in recommend:
                    recommend.append(userg.user)

    random.shuffle(recommend)


    username_profile_list = []

    for user in recommend:
        profile_lists = Profile.objects.filter(user=user)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    comment_list = Comment.objects.all()

    cf = CommentForm()
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'posts': feed,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4],
        'comment_form': cf,
        'comment_list': comment_list,
    }

    return render(request, 'index.html', context)


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        user_prof = Profile.objects.get(user=user)
        list1 = user_prof.followers.all()

        for i in list1:
            profile = Profile.objects.get(user=i)
            if profile.pref is True:
                message = Mail(
                from_email='ivanjosephjacob@gmail.com',
                to_emails=i.email,
                subject='Post',
                html_content=f'<div style="font-family: inherit; text-align: inherit"><span style="font-size: 30px"> {user} has a new post! {caption}</span></div>')
                try:
                    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e.message)

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def comment(request, pk):

    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(pk=pk)
        comment = request.POST['content']

        new_comment = Comment.objects.create(
            user=user, post=post, comment=comment)
        new_comment.save()

    return redirect('/')


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        # username_profile = []
        username_profile_list = []

        # for users in username_object:
        #     username_profile.append(users.id)

        for user in username_object:
            profile_lists = Profile.objects.filter(user=user)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


@login_required(login_url='signin')
def like_post(request):
    user_object = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user_object)
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like_filter = post.liked_post.filter(user=request.user)
    profile2 = post.user.profile.first()
    print(profile2)

    if not like_filter.exists():
        profile.likes.add(post)
        post.no_likes = post.no_likes+1
        post.save()
    
    else:
        profile.likes.remove(post)
        post.no_likes = post.no_likes-1
        post.save()

    if 'profile' in request.META.get('HTTP_REFERER'):
        return redirect(request.build_absolute_uri(reverse('profile', args=(profile2.user.username, ))))
    else:
        return redirect('/')
     

@login_required(login_url='signin')
def flag_post(request):
    user_object = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user_object)
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    flag_filter = post.flagged_post.filter(user=request.user)
    profile2 = post.user.profile.first()

    if not flag_filter.exists():
        profile.flagsp.add(post)
        post.no_flags = post.no_flags+1
        post.save()
        messages.info(request, 'Flagged Post')
        
    else:
        profile.flagsp.remove(post)
        post.no_flags = post.no_flags-1
        post.save()
        messages.info(request, 'Unflagged Post')
    if 'profile' in request.META.get('HTTP_REFERER'):
        return redirect(request.build_absolute_uri(reverse('profile', args=(profile2.user.username, ))))
    else:
        return redirect('/')


@login_required(login_url='signin')
def flag_comment(request):
    user_object = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user_object)
    comment_id = request.GET.get('comment_id')

    comment = Comment.objects.get(id=comment_id)
    flag_filter = comment.flagged_comment.filter(user=request.user)
    profile2 = comment.post.user.profile.first()

    if not flag_filter.exists():
        profile.flagsc.add(comment)
        comment.no_flags_c = comment.no_flags_c+1
        comment.save()
        messages.info(request, 'Flagged Comment')
        
    else:
        profile.flagsc.remove(comment)
        comment.no_flags_c = comment.no_flags_c-1
        comment.save()
        messages.info(request, 'Unflagged Post')
    if 'profile' in request.META.get('HTTP_REFERER'):
        return redirect(request.build_absolute_uri(reverse('profile', args=(profile2.user.username, ))))
    else:
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_post_length = len(user_posts)

    follower = request.user.profile.first()

    if follower.user in user_profile.followers.filter():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = user_profile.followers.count()
    user_following = user_profile.following.count()

    comment_list = Comment.objects.all()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'comment_list': comment_list,


    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        name = request.POST['user']
        username = User.objects.get(username=name)
        user = Profile.objects.get(user=username)
        follower = request.user.profile.first()

        if follower.user in user.followers.filter():
            user.followers.remove(follower.user)
            user.save()
            follower.following.remove(user.user)
            follower.save()
            return redirect('/profile/'+user.user.username)
        else:
            user.followers.add(follower.user)
            user.save()
            follower.following.add(user.user)
            follower.save()
            return redirect('/profile/'+user.user.username)
    else:
        return redirect('/')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('/')
    return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def delete(request, delete_id):
    Post.objects.get(pk=delete_id).delete()
    if 'profile' in request.META.get('HTTP_REFERER'):
        return redirect('profile', request.user.username)
    else:
        return redirect('flag_admin')

@login_required(login_url='signin')
def delete_c(request, delete_c_id):
    Comment.objects.get(pk=delete_c_id).delete()
    return redirect('flag_admin')


class EditPostView(UpdateView):
    model = Post
    template_name = 'edit.html'
    form_class = EditForm
    success_url = '/'


@login_required(login_url='signin')
def pref(request):
    form_class = PrefForm
    form = form_class(request.POST or None)

    if request.method == 'POST':

        user_profile = Profile.objects.get(user=request.user)
        pref = request.POST.get('pref')
        if pref == 'on':
            pref = True
        else:
            pref = False
        user_profile.pref = pref
        user_profile.save()
        return render(request, 'pref.html', {'form': form, 'pref': pref})

    else:
        return render(request, 'pref.html', {'form': form})


def data(request):
    response = HttpResponse(content_type='text/csv')
    response['Contetnt-Disposition'] = 'attachments; filename=user_data.csv'
    writer = csv.writer(response)
    users = User.objects.all()
    writer.writerow(['Username', 'Email', 'Date joined'])
    for user in users:
        writer.writerow([user.username, user.email, user.date_joined])
    return response


@login_required(login_url='signin')
def flag_admin(request):



    context = {
        'flagged_list_p': Post.objects.filter(no_flags__gt=0).order_by('-no_flags'),
        'flagged_list_c': Comment.objects.filter(no_flags_c__gt=0).order_by('-no_flags_c'),
    }

    return render(request, 'flag_admin.html', context)