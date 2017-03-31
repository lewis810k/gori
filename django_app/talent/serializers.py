from rest_framework import serializers

from member.serializers import TutorSerializer
from talent.models import Talent, ClassImage, Curriculum, Location
from member.models import Tutor


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


class TalentListSerializers(serializers.ModelSerializer):
    tutor_id = serializers.PrimaryKeyRelatedField(
        queryset=Tutor.objects.all(), required=True, source='tutor'
    )
    tutor_name = serializers.PrimaryKeyRelatedField(read_only=True,
                                                    source='tutor.user.name')
    class_image = ClassImageSerializers(many=True, source='classimage_set', read_only=True)
    curriculum = CurriculumSerializers(many=True, source='curriculum_set', read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    category = serializers.ChoiceField(choices=Talent.CATEGORY)

    class Meta:
        model = Talent
        fields = (
            'tutor_id',
            'tutor_name',
            # 'wishlist_user',
            'class_title',
            'category_name',
            'category',
            'class_type',
            'cover_image',
            'price_per_hour',
            'is_soldout',
        )

    def get_category_name(self, obj):
        return obj.get_category_display()



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


class TalentDetailSerializers(serializers.ModelSerializer):
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
