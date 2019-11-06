from rest_framework import serializers
from .models import Website, DataType, SearchGroup, SearchList, FetchInfo


class FetchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FetchInfo
        fields = ('tag_name', 'class_name', 'id_name')


class SearchListSerializer(serializers.ModelSerializer):
    fetch_infos = FetchInfoSerializer(many=True, read_only=True)

    class Meta:
        model = SearchList
        fields = ['fetch_infos']


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = ['name']
        

class SearchGroupSerializer(serializers.ModelSerializer):
    search_lists = SearchListSerializer(many=True, read_only=True)
    group_type = DataTypeSerializer(read_only=True)

    class Meta:
        model = SearchGroup
        fields = ('search_lists', 'group_type')


class WebsiteSerializer(serializers.ModelSerializer):
    search_groups = SearchGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Website
        fields = ('id', 'name', 'url', 'search_groups')



