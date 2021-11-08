from rest_framework import serializers
from .models import Comment, Board

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            "password": {"write_only": True}
        }

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        extra_kwargs = {
            "password": {"write_only": True}
        }
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            comments = instance.comments
            response["comments"] = CommentSerializer(comments, many=True).data
        except:
            response["comments"] = None
        return response

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'title', 'created_at', 'updated_at')