from django.urls import path, include
from . import views
urlpatterns =[
    path("",views.index,name="dr"),
    path("login",views.Login,name="login"),
    path("register",views.register,name="register"),
    path("new_product",views.productInfo,name="productInfo"),
    path("existingproduct",views.existingPro,name="existingPro"),
    path("update",views.update,name="update"),
    path("billing",views.billing,name="billing"),
    path("modDB",views.modDB,name="modDB"),
    path("report",views.displayreport,name="dr"),
    path("logout",views.log_out,name="lo"),
]