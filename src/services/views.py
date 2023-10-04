
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from  App.models import Services
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App.forms import ServicesFilterForm
from App.models import Profile



# ALL SERVICES ------------------------------------------------------------------------------------------------------
def services(request):
    page_title = "Services"
    services = Services.objects.all()
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)
    
    posts_paginator = Paginator(services, 15)
    page_num = request.GET.get('page')
    page = posts_paginator.get_page(page_num)
    
    # FILTER COURSES BY COURSE NAME/TITLE -----------------------------
    form = ServicesFilterForm(request.GET)
    if form.is_valid():
        services_name = form.cleaned_data['services_name']
        if services_name:
            page = services.filter(title=services_name)

    context={
        "page_title":page_title,
        'page':page,
        'form':form,
        'services':services,
        'profile_image':profile_image,
    }
    return render(request, 'services.html', context)




# SERVICES-SINGLE ------------------------------------------------------------------------------------------------------
def services_single(request, services):
    page_title = "Services"
    obj = get_object_or_404(Services, slug=services)
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)

    context={
        "page_title":page_title,
        'obj':obj,
        'profile_image':profile_image,

    }
    return render(request, 'services_single.html', context)




# SERVICES SEARCH ==================================================================================================
def services_search_results(request):
    page_title = "Search Services"
    search_queryset = Services.objects.all()
    
    profile_image = ''
    if request.user.is_authenticated:
        profile_image = Profile.objects.filter(user=request.user)

    # FILTER COURSES BY COURSE NAME/TITLE -----------------------------
    form = ServicesFilterForm(request.GET)
    if form.is_valid():
        services_name = form.cleaned_data['services_name']
        if services_name:
            search_queryset = search_queryset.filter(title=services_name)
    
    query = request.GET.get('q')
    if query:
        search_queryset = search_queryset.filter(
            Q(title__icontains=query) |
            Q(introduction__icontains=query) |
            Q(title_summary__icontains=query) |
            Q(main_title__icontains=query) |
            
            Q(key_features_1_title__icontains=query) |
            Q(key_features_1_summary__icontains=query) |
            Q(key_features_2_title__icontains=query) |
            Q(key_features_2_summary__icontains=query) |
            Q(key_features_3_title__icontains=query) |
            Q(key_features_3_summary__icontains=query) |
            Q(key_features_4_title__icontains=query) |
            Q(key_features_4_summary__icontains=query) |
            Q(key_features_5_title__icontains=query) |
            Q(key_features_5_summary__icontains=query) |
            Q(key_features_6_title__icontains=query) |
            Q(key_features_6_summary__icontains=query) |
            
            Q(side_title__icontains=query) |
            Q(side_summary__icontains=query) |
            
            Q(side_key_point_1__icontains=query) |
            Q(side_key_point_2__icontains=query) |
            Q(side_key_point_3__icontains=query) |
            Q(side_key_point_4__icontains=query) 
        ).distinct()
        
    context = {
        'search_queryset': search_queryset,
        'page_title':page_title,
        'form':form,
        'services':services,
        'profile_image':profile_image,
    }
    return render(request, 'services_search_results.html', context)


