from rest_framework import serializers
from semanticsearch.models import Search

class QuerySerializer(serializers.ModelSerializer):
    query = serializers.CharField(max_length=280, allow_blank=False)
    class Meta:
        model = Search
        fields = ['query']