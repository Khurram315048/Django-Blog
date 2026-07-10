from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify




class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural='categories'


    def __str__(self):
        return self.category_name


STATUS_CHOICES=(
    ("Draft","Draft"),
    ("Published","Published")
)        

class Blog(models.Model):
    title=models.CharField(max_length=500)
    slug=models.SlugField(max_length=150,unique=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    featured_image=models.ImageField(upload_to='uploads/%Y/%m/%d')
    short_description=models.TextField(max_length=500)
    blog_body=models.TextField(max_length=2000)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="Draft")
    is_featured=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    



class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment=models.TextField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
