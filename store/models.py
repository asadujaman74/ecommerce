from django.db import models
from django.urls import reverse #for dynamics urls
# Create your models here.

#category model
class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True) 
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = 'categories'  #replace Categorys to categories in DB table

    def __str__(self):
        return self.name
    
    #Dynamic urls Categories wise product show
    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])

#products models     
class Product(models.Model):
    #FK for link up Product model to Category
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null= True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(unique=True) #unique=True means its optional
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/') #root a ekta media folder er modde images folder create hobe autometic then er modde images store hobe   

    class Meta:
        verbose_name_plural = 'products'
    
    def __str__(self):
        return self.title
    
    #Dynamic urls
    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])

    

