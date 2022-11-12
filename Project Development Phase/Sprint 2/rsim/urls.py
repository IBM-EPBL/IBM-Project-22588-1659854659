from django.urls import path, include
from . import views
urlpatterns =[
    path("",views.displayreport,name="dr"),
    path("login",views.Login,name="login"),
    path("register",views.register,name="register"),
    path("new_product",views.productInfo,name="productInfo"),
    path("existingproduct",views.existingPro,name="existingPro"),
]