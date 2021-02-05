from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
#from .views import post

app_name = 'home'

urlpatterns=[
    path('',views.IndexView.as_view(), name='home'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('profile/',views.Profile.as_view(), name ='profile'),
    path('profile/delete/object/<slug:slug>/',views.Profile.as_view(), name ='cancel'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    path('signup/',views.SignupView.as_view(), name='signup'),
    path('available/',views.Available.as_view(),name='available'),
    path('rent/', views.RentVehicles.as_view(), name='rent'),
    path('reservation/<slug>', views.ReservationDetailView.as_view(), name='reservation'),
    path('reservation-update/<slug:slug>', views.UpdateOrder.as_view(), name='reservation-update'),
    path ('renterprofile/',views.RenterProfile.as_view(),name = 'renter-profile'),
    path ('approverent/<slug:slug>/',views.RenterApproval.as_view(),name = 'approve-rent')
    # path('search/',views.SearchView.as_view(),name = 'search'),

]