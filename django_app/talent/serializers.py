from rest_framework import serializers

from member.models import GoriUser
from member.serializers import TutorSerializer
from talent.models import Talent, ClassImage, Curriculum, Location, WishList, Registration


class ClassImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClassImage
        fields = (
            'talent',
            'image'
        )


class LocationSerializers(serializers.ModelSerializer):
    registration_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Location
        fields = (
            'region',
            'talent',
            'registered_student',
            'specific_location',
            'registration_count',
        )

    def get_registration_count(self, obj):
        return obj.registration_set.count()


class CurriculumSerializers(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = (
            'talent',
            'information',
            'image',
        )


class WishListSerializers(serializers.ModelSerializer):
    talent = serializers.PrimaryKeyRelatedField(queryset=Talent.objects.all(), write_only=True)
    talent_title = serializers.PrimaryKeyRelatedField(read_only=True, source='talent.class_title')
    user = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), write_only=True)
    user_name = serializers.PrimaryKeyRelatedField(read_only=True, source='user.name')

    class Meta:
        model = WishList
        fields = (
            'talent',
            'talent_title',
            'user_name',
            'user',
            'added_date'
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=WishList.objects.all(),
                fields=('talent', 'user'),
                message=("Some custom message.")
            )
        ]


class LocationListSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return '{}'.format(value.get_region_display())


class TalentListSerializers(serializers.ModelSerializer):
    # tutor_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Tutor.objects.all(), required=True, source='tutor'
    # )
    # tutor_name = serializers.PrimaryKeyRelatedField(read_only=True,
    #                                                 source='tutor.user.name')
    tutor = TutorSerializer()
    category_name = serializers.SerializerMethodField(read_only=True)
    category = serializers.ChoiceField(choices=Talent.CATEGORY, write_only=True)
    class_type_name = serializers.SerializerMethodField(read_only=True)
    class_type = serializers.ChoiceField(choices=Talent.CLASS_TYPE_CHOICE, write_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    # location = serializers.SlugRelatedField(read_only=True,many=True,slug_field='region')
    locations = LocationListSerializer(queryset=Location.objects.all(), many=True)

    # registeredstudent = RegisteredStudentSeriaLizer(queryset=Location.objects.all(), many=True)

    # wishlist_user = serializers.StringRelatedField(many=True, source='wishlist_set', read_only=True)

    class Meta:
        model = Talent
        fields = (
            'tutor',
            'class_title',
            'category_name',
            'category',
            'class_type_name',
            'class_type',
            'cover_image',
            'price_per_hour',
            'is_soldout',
            'created_date',
            'review_count',
            'locations',
            'registration_count',
        )

    def get_category_name(self, obj):
        return obj.get_category_display()

    def get_class_type_name(self, obj):
        return obj.get_class_type_display()

    def get_review_count(self, obj):
        return obj.review_set.count()


class TalentDetailSerializers(serializers.ModelSerializer):
    class_image = ClassImageSerializers(many=True, source='classimage_set', read_only=True)
    curriculum = CurriculumSerializers(many=True, source='curriculum_set', read_only=True)
    wishlist_user = serializers.StringRelatedField(many=True, source='wishlist_set', read_only=True)

    class Meta:
        model = Talent
        fields = (
            'tutor',
            'wishlist_user',
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


class TalentCrateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Talent
        fields = (
            'tutor',
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
        )


class RegistrationSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=GoriUser.objects.all(), source='student.name')
    talent_location = LocationListSerializer(read_only=True)
    student_level = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Registration
        fields = (
            'student',
            'talent_location',
            'joined_date',
            'is_confirmed',
            'student_level',
            'experience_length',
            'message_to_tutor',
        )

    def get_student_level(self, obj):
        return obj.get_student_level_display()
