from rest_framework import serializers

from member.serializers import TutorSerializer
from talent.models import Talent, Curriculum, Location
from talent.serializers import LocationSerializer
from utils import review_average_rate
from .class_image import ClassImageSerializer
from .curriculum import CurriculumSerializer

__all__ = (
    'TalentListSerializer',
    'TalentShortInfoSerializer',
    'TalentCrateSerializers',
    'TalentDetailSerializer',
    'TalentShortDetailSerializer',
)


class TalentShortInfoSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    regions = serializers.SerializerMethodField(read_only=True)
    average_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'category',
            'type',
            'cover_image',
            'price_per_hour',
            'is_soldout',
            'is_verified',
            'created_date',
            'average_rate',
            'review_count',
            'registration_count',
            'regions',
        )

    def get_category(self, obj):
        return obj.get_category_display()

    def get_type(self, obj):
        return obj.get_type_display()

    def get_review_count(self, obj):
        return obj.reviews.count()

    def get_regions(self, obj):
        return obj.region_list

    @staticmethod
    def get_average_rate(obj):
        return review_average_rate(obj.reviews)


class TalentListSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    # category = serializers.ChoiceField(choices=Talent.CATEGORY, write_only=True)
    # type_name = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    regions = serializers.SerializerMethodField(read_only=True)
    is_school = serializers.SerializerMethodField(read_only=True)
    average_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            # 'category_name',
            'category',
            # 'type_name',
            'type',
            'tutor',
            'is_school',
            'cover_image',
            'price_per_hour',
            'hours_per_class',
            'number_of_class',
            'min_number_student',
            'max_number_student',
            'is_verified',
            'is_soldout',
            'created_date',
            'average_rate',
            'review_count',
            'registration_count',
            'regions',

        )

    def get_category(self, obj):
        return obj.get_category_display()

    def get_type(self, obj):
        return obj.get_type_display()

    def get_review_count(self, obj):
        return obj.reviews.count()

    def get_regions(self, obj):
        return obj.region_list

    def get_is_school(self, obj):
        is_school = False
        school_list = [school[1] for school in Location.SCHOOL]
        for item in obj.region_list:
            if item in school_list:
                is_school = True
                break
        return is_school

    @staticmethod
    def get_average_rate(obj):
        return review_average_rate(obj.reviews)


class TalentShortDetailSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    average_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        depth = 1
        model = Talent
        fields = (
            'pk',
            'title',
            'tutor',
            'category',
            'type',
            'tutor_message',
            'cover_image',
            'tutor_info',
            'class_info',
            'average_rate',
            'review_count',
            'registration_count',
            'video1',
            'video2',
            'price_per_hour',
            'hours_per_class',
            'number_of_class',
            'min_number_student',
            'max_number_student',
            'is_soldout',
            'is_verified',

        )

    def get_category(self, obj):
        return obj.get_category_display()

    def get_type(self, obj):
        return obj.get_type_display()

    def get_review_count(self, obj):
        return obj.reviews.count()

    @staticmethod
    def get_average_rate(obj):
        return review_average_rate(obj.reviews)


class TalentDetailSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(read_only=True)
    class_images = ClassImageSerializer(many=True, source='classimage_set', read_only=True)
    curriculums = CurriculumSerializer(many=True, source='curriculum_set', read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    average_rate = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    # category = serializers.ChoiceField(choices=Talent.CATEGORY)
    locations = LocationSerializer(many=True)
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        depth = 1
        model = Talent
        fields = (
            'pk',
            'title',
            'tutor',
            # 'category_name',
            'tutor_message',
            'category',
            'type',
            'average_rate',
            'review_count',
            'registration_count',
            'cover_image',
            'tutor_info',
            'class_info',
            'video1',
            'video2',
            'locations',
            'price_per_hour',
            'hours_per_class',
            'number_of_class',
            'min_number_student',
            'max_number_student',
            'is_soldout',
            'is_verified',
            'class_images',
            'curriculums',
        )

    def get_category(self, obj):
        return obj.get_category_display()

    @staticmethod
    def get_average_rate(obj):
        return review_average_rate(obj.reviews)

    def get_review_count(self, obj):
        return obj.reviews.count()

    def get_type(self, obj):
        return obj.get_type_display()

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.type = validated_data.get('type', instance.type)
        instance.cover_image = validated_data.get('cover_image', instance.cover_image)
        instance.tutor_info = validated_data.get('tutor_info', instance.tutor_info)
        instance.class_info = validated_data.get('class_info', instance.class_info)
        instance.video1 = validated_data.get('video1', instance.video1)
        instance.video2 = validated_data.get('video2', instance.video2)
        instance.price_per_hour = validated_data.get('price_per_hour', instance.price_per_hour)
        instance.hours_per_class = validated_data.get('hours_per_class', instance.hours_per_class)
        instance.number_of_class = validated_data.get('number_of_class', instance.number_of_class)
        instance.save()
        print(self.initial_data)
        for index, image in enumerate(self.initial_data.get(
                'c1', validated_data['curriculum_set'])):
            item = Curriculum.objects.filter(talent=instance)[index]
            item.image = image
            # item.image = new_image
            item.save()
            # print(image)
            # print(self.initial_data['curriculum1'])
            # photos = self.initial_data['curriculum_set']
            # print(photos)
            # if validated_data:
            #     print("vd {}".format(validated_data))
            # class_images = validated_data.get('classimage_set', instance.classimage_set)
            # print("cl {} ".format(class_images))
            # if validated_data.get['classimage_set']:
            #     for index, new_class_image in enumerate(validated_data['classimage_set']):
            #         new_image = new_class_image.get["image"]
            #         item = ClassImage.objects.filter(talent=instance)[index]
            #         item.image = new_image
            #         item.save()

            # if validated_data['curriculum_set']:
        for index, new_curriculum_item in enumerate(validated_data.pop('curriculum_set')):
            print(new_curriculum_item)
            new_info = new_curriculum_item["information"]
            # new_image = new_curriculum_item["image"]
            item = Curriculum.objects.filter(talent=instance)[index]
            item.information = new_info
            # item.image = new_image
            item.save()

        return instance


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


class TalentCrateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Talent
        fields = (
            'tutor',
            'title',
            'category',
            'type',
            'tutor_message',
            'cover_image',
            'tutor_info',
            'class_info',
            'video1',
            'video2',
            'price_per_hour',
            'hours_per_class',
            'number_of_class',
            'min_number_student',
            'max_number_student',
            'is_soldout',
            'is_verified',
        )
