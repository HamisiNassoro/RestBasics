#--------------------urls for function based views------------------------------

from django.urls import path
from .views import article_list, article_detail

urlpatterns = [
    path('article/', article_list),
    path('detail/<int:pk>/', article_detail)
    
]

#------------------urls for class based views--------------------------------------

from django.urls import path
from .views import ArticleAPIView, ArticleDetails

urlpatterns = [
    path('article/', ArticleAPIView.as_view()),
    path('detail/<int:id>/', ArticleDetails.as_view())
    
]

#-----------------urls for Generic views and mixins----------------------------------

from django.urls import path
from .views import GenericAPIView

urlpatterns = [
    path('generic/article/<int:id>/', GenericAPIView.as_view()),
    
]

#------------------urls for ViewSets and routers-------------------------------------

from django.urls import path, include
from .views import ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls))

]
