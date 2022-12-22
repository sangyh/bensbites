from rest_framework import serializers
from semanticsearch.models import Search
from semanticsearch.models import Topic

class QuerySerializer(serializers.ModelSerializer):
    query = serializers.CharField(max_length=280, allow_blank=False)
    class Meta:
        model = Search
        fields = ['query']

class TopicSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(max_length=140, allow_blank=True)
    class Meta:
        model = Topic
        fields = ['topic']