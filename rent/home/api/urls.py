from django.urls import path,include
from rest_framework import routers
from home.api.views import (ItemFilterListView)
# router = routers.DefaultRouter()
# router.register('user', UserViewSet)

urlpatterns=[
    # path('',include (router.urls)),
    path('item/',ItemFilterListView.as_view(),name='item'),
]