from django.urls import path     
from . import views

urlpatterns = [
    path('home', views.home),
    path('addWish',views.addWish),
    path('createWish',views.createWish),
    path('<id>/stats',views.stats),
    path('<id>/edit',views.editWish),
    path('<id>/update',views.updateWish),
    path('<id>/like',views.likeWish),
    path('<id>/destroy',views.destroyWish),
    path('<id>/grant',views.grant),
    
    # path('granted', views.granted)

]