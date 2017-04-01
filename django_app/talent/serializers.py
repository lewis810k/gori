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


#
# class TalentListingField(serializers.RelatedField):
#     @staticmethod
#     def get_choices_value(key, CHOICE):
#         for item in CHOICE:
#             if key in item:
#                 _, value = item
#                 return value
#
#     def to_representation(self, value):
#         category = self.get_choices_value(value.category, Talent.CATEGORY)
#         class_type = self.get_choices_value(value.class_type, Talent.CLASS_TYPE_CHOICE)
#         custom_fields = {
#             'id': value.id,
#             'title': value.class_title,
#             'category': category,
#             'class_type': class_type,
#         }
#         return custom_fields


class LocationSerializers(serializers.ModelSerializer):
    region = serializers.SerializerMethodField(read_only=True)
    specific_location = serializers.SerializerMethodField(read_only=True)
    day = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Location
        fields = (
            # 'talent',
            'region',
            'specific_location',
            'registered_student',
            'day',
            'time',
            'extra_fee',
            'extra_fee_amount',
        )

    @staticmethod
    def get_region(obj):
        return obj.get_region_display()

    @staticmethod
    def get_specific_location(obj):
        return obj.get_specific_location_display()

    @staticmethod
    def get_day(obj):
        return obj.get_day_display()


class LocationWrapperSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    class_type = serializers.SerializerMethodField(read_only=True)
    locations = LocationSerializers(many=True)

    class Meta:
        model = Talent
        fields = (
            'id',
            'class_title',
            'category',
            'class_type',
            'locations',
        )

    @staticmethod
    def get_category(obj):
        return obj.get_category_display()

    @staticmethod
    def get_class_type(obj):
        return obj.get_class_type_display()
