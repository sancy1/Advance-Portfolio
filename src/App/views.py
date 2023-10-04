from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import is_superuser
from django.db.models import Count, Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.views.generic import TemplateView

from .models import About, Services, Experience, Blog, Tag, Category, Author, Subscribe, MyCv, Profile
from App.forms import BlogFilterForm, SubscribeForm

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm




#========================================================================================================


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})




# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)




class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')




class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')




@login_required
def profile(request):
    page_title = "Profile"
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
        
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users_dashboard')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'profile_image':profile_image, 'page_title':page_title})




# USERS-DASHBOARD ----------------------------------------------------------
def users_dashboard(request):
    page_title = "Dashboard"
    
    
    new = ''
    if request.user.is_authenticated:
        new = new = Blog.newmanager.filter(favourites=request.user)[:2]
        
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
        
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users_dashboard')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    
    context = {
        'page_title':page_title,
        'profile_image':profile_image,
        'user_form': user_form, 
        'profile_form': profile_form,
        'new':new,
    }
    return render(request, 'users/users_dashboard.html', context )

    
#========================================================================================================




# ADMIN LOGIN WITH FUNCTION-------------------------------------------------------------------------------------------
def admin_login(request):
    page_title = "Alex's Login"
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                messages.info(request, f"Welcome! You are now logged in as @{username}.")
                if request.user.is_superuser:
                    return redirect("admin_dashboard")
                else:
                    messages.info(request,"Invalid User! This Login page is restricted to admin only.")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="admin_login.html", context={"login_form":form, "page_title":page_title})




# ADMIN DASHBOARD ------------------------------------------------------------------------------------------------------
@login_required(login_url='admin_login')
@is_superuser
def admin_dashboard(request):
    if request.user.is_superuser:
        page_title = "Admin-Dashboard"

        context={
            "page_title":page_title,

        }
    else:
        return HttpResponseForbidden("Access denied. This page is restricted to admin user only ")
    return render(request, 'admin_dashboard.html', context)




def signin_option(request):
    page_title = "Signin option"
    template = "signin_option.html"
    context = {
                'page_title':page_title,
               }
    return render(request, template, context)




# HOMEPAGE ------------------------------------------------------------------------------------------------------
def home(request):
    page_title = "Alex Portfolio"
    
    about = About.objects.all()
    home_services = Services.objects.all()[:6]
    experience = Experience.objects.all()
    blog = Blog.objects.all()[:3]
    
    pdf_documents = MyCv.objects.all()[1:2]
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)

    context={
        "page_title":page_title,
        "about":about,
        "home_services":home_services,
        "experience":experience,
        "blog":blog,
        'pdf_documents':pdf_documents,
        'profile_image':profile_image,
    }
    return render(request, 'home.html', context)




# BLOG ------------------------------------------------------------------------------------------------------
def blog(request):
    page_title = "Blog"
    
    blog =  Blog.objects.all()
    category_list = Category.objects.exclude(name='default')
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
    
    posts_paginator = Paginator(blog, 15)
    page_num = request.GET.get('page')
    page = posts_paginator.get_page(page_num)
    
    # FILTER COURSES BY COURSE NAME/TITLE -----------------------------
    form = BlogFilterForm(request.GET)
    if form.is_valid():
        blog_name = form.cleaned_data['blog_name']
        if blog_name:
            page = blog.filter(title=blog_name)
            

    context={
        "page_title":page_title,
        "blog":blog,
        'category_list':category_list,
        'page':page,
        'form':form,
        'profile_image':profile_image,

    }
    return render(request, 'blog.html', context)




# TAG -------------------------------------------------------------------------------
def tag_blog(request, blog_tag):
    page_title = "Tags"
    category_list = Category.objects.exclude(name='default')
    
    tag = Tag.objects.get(name=blog_tag)
    tagged_posts = Blog.objects.filter(tags=tag)
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
    
    context = {
        'page_title':page_title,
        'category_list':category_list,
        'tag': tag, 
        'tagged_posts': tagged_posts,
        'profile_image':profile_image,
        }
    return render(request, 'tag_blog.html', context)




from django.db.models import Count 
# SINGLE BLOG PAGE -------------------------------------------------------------------------------
def blog_single(request, blog):
    page_title = "Blog Single"
    
    blog = get_object_or_404(Blog, slug=blog, status='published')
    recent_blog =  Blog.objects.order_by('-publish')[:4]
    
    # Cattegory without count
    category_list = Category.objects.exclude(name='default')
    # Cattegory with count
    categories_with_counts = Category.objects.annotate(blog_count=Count('blog'))
    
    # Automatic Next & Previous Post
    next_post = Blog.objects.filter(publish__gt=blog.publish).order_by('publish').first()
    previous_post = Blog.objects.filter(publish__lt=blog.publish).order_by('-publish').first()
    
    # Favourite
    # new = Blog.objects.filter(favourites=request.user)[:2]
    new = ''
    if request.user.is_authenticated:
        new = Blog.objects.filter(favourites=request.user)[:2]
        
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
    
    # FAVOURITES
    fav = bool
    if blog.favourites.filter(id=request.user.id).exists():
        fav = True
    
    # HIT-COUNT WITH FUNCTION VIEWS
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(blog)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    context = {
        'blog': blog, 
        'page_title':page_title, 
        'category_list': category_list, 
        "recent_blog":recent_blog, 
        'fav':fav,
        'new':new,
        
        'categories_with_counts':categories_with_counts,
        'next_post':next_post,
        'previous_post':previous_post,
        'profile_image':profile_image,
        }
    return render(request, 'blog_single.html', context)




# ADD FAVORITE OR REMOVE BLOG =====================================================================================
@login_required
def favourite_list(request):
    page_title = "Favourite"
    new = Blog.newmanager.filter(favourites=request.user)
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)

    context = {
        'page_title':page_title,
        'new':new,
        'profile_image':profile_image,
        }
    return render(request, 'favourites.html', context)



@login_required
def favourite_add(request, id):
    blog = get_object_or_404(Blog, id=id)
    
    if blog.favourites.filter(id=request.user.id).exists():
        blog.favourites.remove(request.user)
    else:
        blog.favourites.add(request.user)
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




# BLOG CATEGORY -------------------------------------------------------------------------------
def category(request, category):
    page_title = "Blog Category"
    template_name = 'category.html'
    paginate_by = 9
    
    catlist = Blog.objects.filter(blog_category__name=category).filter(status='published')
    category_list = Category.objects.exclude(name='default')
    blog = Blog.objects.all()
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
    
    posts_paginator = Paginator(catlist, paginate_by)
    page_num = request.GET.get('page')
    page = posts_paginator.get_page(page_num)
    
    # FILTER COURSES BY COURSE NAME/TITLE -----------------------------
    form = BlogFilterForm(request.GET)
    if form.is_valid():
        blog_name = form.cleaned_data['blog_name']
        if blog_name:
            page = blog.filter(title=blog_name)
            
    
    context = {
        'count':posts_paginator.count,
        'page':page,
        "page_title": page_title,
        "category": category,
        "catlist": catlist,
        "category_list": category_list,
        'form': form,
        'profile_image':profile_image,
    }
    
    return render(request, template_name, context) 




# BLOG SEARCH ==================================================================================================
def search_results(request):
    page_title = "Search Blog"
    search_queryset = Blog.objects.all()
    category_list = Category.objects.exclude(name='default')
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)

    # FILTER COURSES BY COURSE NAME/TITLE -----------------------------
    blog = ''
    form = BlogFilterForm(request.GET)
    if form.is_valid():
        blog_name = form.cleaned_data['blog_name']
        if blog_name:
            search_queryset = search_queryset.filter(title=blog_name)
    
    query = request.GET.get('q')
    if query:
        search_queryset = search_queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(highlight__icontains=query) |
            Q(content1__icontains=query) 
        ).distinct()
        
    context = {
        'search_queryset': search_queryset,
        'page_title':page_title,
        'category_list':category_list,
        'form':form,
        'blog':blog,
        'profile_image':profile_image,
    }
    return render(request, 'search_results.html', context)





# CONTACT ------------------------------------------------------------------------------------------------------
def contact(request):
    page_title = "Contact"
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        form_data = {
            'name':name,
            'phone':phone,
            'email':email,
            'subject':subject,
            'message':message,
        }
        
        message = '''
        Name: {}
        Phone: {}
        Email: {}\n
        Subject: {}
        \n{}
        
        '''.format(form_data['name'], form_data['phone'], form_data['email'], form_data['subject'], form_data['message'])
        send_mail(subject, message, '', ['<sanchez.alexander.cyril@gmail.com>'])
        
        return render(request, 'success.html', {})
    return render(request, 'contact.html', {'page_title':page_title, 'profile_image':profile_image,})




# SUCCESS FOR CONTACT PAGE ------------------------------------------------------------------
def success(request):
    page_title = "Success"
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
        
    context = {
                'page_title':page_title, 
                'profile_image':profile_image,
               }
    return render(request, "success.html", context)




# PDF FILE ----------------------------------------------------------------------------------------
# def pdf_list(request):
    # if request.method == 'POST':
    #     form = PDFUploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    # else:
    #     form = PDFUploadForm()
    
    # 'form': form
    
    # pdf_documents = MyCv.objects.all()
    # return render(request, 'cv_file.html', {'pdf_documents': pdf_documents})




#SUBSCRIBE ------------------------------------------------------------------------------------------------------
def subscribe(request):
    page_title = "Ekisa-Dio Subscribe"
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email', None)

        if not email:
            messages.error(request, "You must type legit email to subscribe to a Newsletter")
            return redirect("/")

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "/")) 

        subscribe_user = Subscribe.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"FAILED! {email} email address is already a subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "/"))  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = Subscribe()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'SUCCESSFUL!! The email address {email} has been successfully subscribed to our newsletter.')
        
        context = {'page_title':page_title, 'profile_image':profile_image,}
        return redirect(request.META.get("HTTP_REFERER", "/"), context)







# views.py

# from django.shortcuts import render

# def profile(request):
#     return render(request, 'profile.html')
