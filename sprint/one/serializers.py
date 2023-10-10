from .models import *
from rest_framework import serializers


# class UsersSerializer(serializers.ModelSerializer):
# class UsersSerializer(serializers.HyperlinkedModelSerializer):

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climber
        fields = ['surname', 'name', 'patronymic', 'email', 'telephone']


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'spring', 'summer', 'autumn']


class ImageSerializer(serializers.ModelSerializer):
    # photo = serializers.CharField()
    class Meta:
        model = Image
        fields = ['title1', 'photo1', 'title2', 'photo2', 'title3', 'photo3', 'title4', 'photo4']


class PeakSerializer():
    # class PeakSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()
    coords = CoordinateSerializer()
    level = LevelSerializer()
    images = ImageSerializer()

    class Meta:
        model = Peak
        fields = ['country', 'category', 'title', 'other_titles', 'connect', 'add_time', 'status', 'activities', 'user',
                  'coords', 'level',
                  'images']

    def create(self, validated_data, **kwargs):
        user_data = validated_data.pop('user')
        images_data = validated_data.pop('images')
        coordinates_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')

        current_user = Climber.objects.filter(email=user_data['email'])
        if current_user.exists():
            user_serializer = AuthorSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_data = user_serializer.save()
        else:
            user_data = Climber.objects.create(**user_data)

        # user = Author.objects.create(**user_data)
        coords = Coordinate.objects.create(**coordinates_data)
        level = Level.objects.create(**level_data)
        images = Image.objects.create(**images_data)

        peak = Peak.objects.create(**validated_data, user=user_data, coords=coords, level=level, images=images)

        peak.save()
        return peak
