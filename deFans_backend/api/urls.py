from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('', include(router.urls)),
    # path('room', RoomView.as_view())
]
