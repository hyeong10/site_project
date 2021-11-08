from django.urls import include, path
from rest_framework import routers
from board import views

router = routers.DefaultRouter()
router.register(r'board', views.BoardViewSet) #generates routes for a standard set of create/retrieve/update/destroy style actions

urlpatterns = [
    path('', include(router.urls)),
    path('comment/', views.CommentCreateView.as_view()),
    path('comment/<pk>/', views.CommentView.as_view()),
]