from django.urls import path
from . import views
urlpatterns =[
    path("",views.displayreport,name="dr"),
    path("new_product",views.productInfo,name="productInfo"),
    path("existingproduct",views.existingPro,name="existingPro"),
]