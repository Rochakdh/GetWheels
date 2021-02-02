from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
#from .views import post

app_name = 'home'

urlpatterns=[
    path('',views.IndexView.as_view(), name='home'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    path('signup/',views.SignupView.as_view(), name='signup'),
    path('available/',views.Available.as_view(),name='available'),
    path('rent/', views.RentVehicles.as_view(), name='rent'),
    path('reservation/<slug>', views.ReservationDetailView.as_view(), name='reservation'),
    # path('search/',views.SearchView.as_view(),name = 'search'),

]