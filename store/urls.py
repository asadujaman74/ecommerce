from django.urls import path
from . import views

urlpatterns = [

    #store main page
    path('',views.store , name= 'store'),

    #Indivisual product urls
    path('product/<slug:product_slug>/',views.product_info , name= 'product-info'),

    #Indivisual Category urls
    path('search/<slug:category_slug>/',views.list_category , name= 'list-category'),

]