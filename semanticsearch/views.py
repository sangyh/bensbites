from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from semanticsearch.models import Search
from semanticsearch.serializers import QuerySerializer
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

        # Do some processing with the search query
        # ...

        # Return a response to the frontend in this format
        '''data=[{'blog':'', 'text':'', 'extlink':''},
                {'blog':'', 'text':'', 'extlink':''}]
        '''

        data = run_query.main(query)
        return Response(data, content_type='application/json')