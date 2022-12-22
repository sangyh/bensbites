from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from semanticsearch.models import Search
from semanticsearch.models import Topic
from semanticsearch.serializers import QuerySerializer, TopicSerializer
from rest_framework.response import Response
import ML_files.run_query as run_query

class QueryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows results to be viewed
    """

    queryset = Search.objects.all()
    serializer_class = QuerySerializer
    
    
    def list(self, request):
        # Get the search query from the request object
        query = request.GET.get('q')
        print('this is the search query:', query)

        # Return a response to the frontend in this format
        '''data=[{'blog':'', 'text':'', 'extlink':''},
                {'blog':'', 'text':'', 'extlink':''}]
        '''

        data = run_query.get_search_results(query)
        return Response(data, content_type='application/json')

class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows results to be viewed
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    
    def list(self, request):
        # Get the search query from the request object

        data = run_query.get_topics()
        return Response(data, content_type='application/json')

class FilterTopicsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows results to be viewed
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    
    def list(self, request):
        # Get the search query from the request object
        topic = request.GET.get('q')

        data = run_query.filter_topics(topic)
        return Response(data, content_type='application/json')