from rest_framework import serializers
from .models import Monster

class MonsterSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Monster
        fields = ['id', 'name', 'level', 'exp_earn', 'hp', 'attack', 'defense', 'image', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
