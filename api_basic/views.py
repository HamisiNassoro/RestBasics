from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view #added to be used for api_view()decorators
from rest_framework.response import Response #added to be used for api_view()decorators
from rest_framework import status #added to be used for api_view()decorators
from rest_framework.views import APIView #added to be used in class based 
from .models import Article
from .serializers import ArticleSerializer

# Create your views here.

#-----------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------ModalViewSets--------------------------------------------------------

#N/B---- comment out (Viewsets and Routers) and also (Generic ViewSets)-----------------and uses the same urls.py/api_basic for Viewsets & routers-------------

#-----------------------------------------------------------------------------------------------------------------------

from rest_framework import viewsets

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()





#-----------------------------------------------------------------------------------------------------------------------

#---------------------------------------------Generic ViewSets---------------------------------------------------------

#N/B---- comment out Viewsets and Routers-----------------and uses the same urls.py/api_basic for Viewsets & routers-----

#-----------------------------------------------------------------------------------------------------------------------

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import mixins

class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()





#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------------Viewsets & routers----------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------

from rest_framework import viewsets
from django.shortcuts import get_object_or_404

class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#-----------authentication------------------------
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------Generic views and mixins---------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------

from rest_framework import generics
from rest_framework import mixins
#write your views
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset =Article.objects.all()

    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'id'

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self,request,id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)











#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------Class Based API Views----------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
from rest_framework.views import APIView
from rest_framework import status


class ArticleAPIView(APIView):
    def get(self, request): 
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#-----------------------------------------------------------------------------------------------------------------------

#---------------------------api_view() Decorator in Function Based API Views-----(i.e) for web browsable-----------------

#-----------------------------------------------------------------------------------------------------------------------

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



@api_view(['GET', 'POST'])
def article_list(request):
    
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
        
    elif request.method ==  'POST':
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request,pk): #check by primary key 
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT': #to update
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#-----------------------------------------------------------------------------------------------------------------------


#---------------------Function Based API Views--------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def article_list(request):
    
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        return JsonResponse(serializer.data, safe = False)
        
    elif request.method ==  'POST':
        data = JSONParser().parse(request)  
        serializer = ArticleSerializer(data=data)   
        

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)   #status = 201, created status
        return JsonResponse(serializer.errors, status=400)
        
@csrf_exempt
def article_detail(request,pk): #check by primary key 
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)  #status = 404, Not found

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT': #to update
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)    #used for function based views
        return JsonResponse(serializer.errors, status=400)    #status = 400, Bad request

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204) #status = 204, no content