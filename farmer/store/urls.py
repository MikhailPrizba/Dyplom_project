from django.urls import path
from . import views
app_name = 'store'
urlpatterns = [
      path('',views.home, name='home'),
      path('<slug:category_slug>/', views.home, name='product_list_by_category'),
      path('<slug:slug>/<int:id>/', views.product_detail, name='product_detail'),
      
]