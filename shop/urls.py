from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.Home,name="home"),
    path("register/",views.Register,name="register"),
    path("login/",views.Login_page,name="login"),
    path("logout/",views.Logout_page,name="logout"),
    path("collections/",views.Collections,name='collections'),
    path("collections/<str:name>",views.Collectionsview,name='collections'),
    path("collections/<str:cname>/<str:pname>",views.Product_details,name='product_details'),
    path("addtocart/",views.Add_to_Cart,name="addtocart")
]