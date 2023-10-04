from django.db import models
from django.urls import reverse
from tinymce.widgets import TinyMCE
from tinymce import models as tinymce_models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User

User = get_user_model()





# Extending User Model Using a One-To-One Link ---------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
            
            
            
            
# ABOUT------------------------------------------------------------------------------------------------
class About(models.Model):
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField()
    image = models.ImageField(null=True, blank=True, upload_to="home/")
    
    key_point_1 = models.CharField(max_length=255)
    key_point_2 = models.CharField(max_length=255)
    key_point_3 = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title




# SERVICES------------------------------------------------------------------------------------------------
class Services(models.Model):
    introduction = models.TextField()
    title = models.CharField(max_length=255)
    title_summary = models.CharField(max_length=255)
    main_title = models.CharField(max_length=255)
    
    #content = tinymce_models.HTMLField()
    image = models.ImageField(null=True, blank=True, upload_to="home/")
    
    # HOW I WORK
    key_features_1_title = models.CharField(max_length=255)
    key_features_1_summary = models.TextField()
    
    key_features_2_title = models.CharField(max_length=255)
    key_features_2_summary = models.TextField()
    
    key_features_3_title = models.CharField(max_length=255)
    key_features_3_summary = models.TextField()
    
    key_features_4_title = models.CharField(max_length=255)
    key_features_4_summary = models.TextField()
    
    key_features_5_title = models.CharField(max_length=255, null=True, blank=True)
    key_features_5_summary = models.TextField(null=True, blank=True)
    
    key_features_6_title = models.CharField(max_length=255, null=True, blank=True)
    key_features_6_summary = models.TextField(null=True, blank=True)
    
    how_i_work_text = models.TextField()
    
    # SIDE-CONTENT
    side_title = models.CharField(max_length=255)
    side_summary = models.TextField()
    
    side_key_point_1 = models.CharField(max_length=255)
    side_key_point_2 = models.CharField(max_length=255)
    side_key_point_3 = models.CharField(max_length=255)
    side_key_point_4 = models.CharField(max_length=255)
    
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('services:services_single', args=[self.slug])
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)




# WORK EXPERIENCE ------------------------------------------------------------------------------------------------
class Experience(models.Model):
    job_title = models.CharField(max_length=255)
    company_and_year = models.CharField(max_length=255)
    job_summary = tinymce_models.HTMLField()
    
    def __str__(self):
        return self.job_title




# SUBSCRIBE ------------------------------------------------------------------------------------------------
class Subscribe(models.Model):    
    email = models.EmailField(max_length = 254, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.email




# MY-CV -------------------------------------------------------------------------------------------------
class MyCv(models.Model): 
    title = models.CharField(max_length=255, blank=True, null=True)
    pdf_file = models.FileField(upload_to='document/', blank=True, null=True)
    def __str__(self):
        return self.title




# AUTHOR ------------------------------------------------------------------------------------------------
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return self.user.username
    
    
    
    
# BLOG CATEGORY ------------------------------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name




# TAGS ------------------------------------------------------------------------------------------------
class Tag(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
    
    
        
# BLOG ------------------------------------------------------------------------------------------------
class Blog(models.Model):
    
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
        
    options = (
            ('draft', 'Draft'),
            ('published', 'Published'),
        )
    
    title = models.CharField(max_length=255)
    overview = tinymce_models.HTMLField()
    highlight = models.CharField(max_length=255)
    content1 = tinymce_models.HTMLField()
    
    image = models.ImageField(upload_to='blog_images/')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    blog_category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    
    tags = models.ManyToManyField(Tag)
    cate_name = models.CharField(max_length=500)
    featured = models.BooleanField(default='Select')
    
    view_count = models.IntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager
    
    slug = models.SlugField(max_length=250, unique=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_single', args=[self.slug])
    
    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.title)
            
    # @property
    # def view_count(self):
    #     return Blog.objects.filter(blog=self).count()
