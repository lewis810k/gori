from rest_framework import serializers

from member.serializers import TutorSerializer
from talent.models import Talent, ClassImage, Curriculum, Location


class ClassImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClassImage
        fields = (
            'talent',
            'image'
        )


class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'region',
            'talent',
            'registered_student',
            'specific_location',
        )


class CurriculumSerializers(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = (
            'talent',
            'information',
            'image',
        )


class TalentSerializers(serializers.ModelSerializer):
    class_image = ClassImageSerializers(many=True, source='classimage_set', read_only=True)
    curriculum = CurriculumSerializers(many=True, source='curriculum_set', read_only=True)

    class Meta:
        model = Talent
        fields = (
            'tutor',
            # 'wishlist_user',
            'class_title',
            'category',
            'class_type',
            'cover_image',
            'tutor_info',
            'class_info',
            'video1',
            'video2',
            'price_per_hour',
            'hours_per_class',
            'number_of_class',
            'is_soldout',
            'class_image',
            'curriculum',
        )


        # def create(self, validated_data):
        #     photos = validated_data.pop('photo_set')
        #     talent = Talent.objects.create(**validated_data)
        #     for photo in photos:
        #         print('photo', photo)
        #         Talent.objects.create(
        #             photo=photo,
        #             post=
        #         )
        #
        #     return post
