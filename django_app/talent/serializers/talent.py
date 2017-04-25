import collections

from rest_framework import serializers

from member.serializers import TutorSerializer
from talent.models import Talent, Curriculum, Location
from utils import review_average_rate, Tutor, get_user_model
from utils.region_display import region_display
from .class_image import ClassImageSerializer
from .curriculum import CurriculumSerializer
from .location import LocationSerializer
from .qna import QuestionSerializer
from .review import ReviewSerializer, AverageRatesSerializer

__all__ = (
    'TalentListSerializer',
    'TalentShortInfoSerializer',
    'TalentCreateSerializer',
    'TalentDetailSerializer',
    'TalentShortDetailSerializer',
    'MyTalentsWrapperSerializer',
    'TalentUpdateSerializer',
)

User = get_user_model()


class TalentShortInfoSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    regions = serializers.SerializerMethodField(read_only=True)
    average_rate = serializers.SerializerMethodField(read_only=True)
    wishlist_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Talent
        fields = (
            'pk',
            'title',
            'view_count',
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
            'wishlist_count',
            'regions',
        )

    def get_category(self, obj):
        return obj.get_category_display()

    def get_type(self, obj):
        return obj.get_type_display()

    def get_review_count(self, obj):
        return obj.reviews.count()

    def get_wishlist_count(self, obj):
        return obj.wishlist_user.count()

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
            'view_count',
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
    average_rates = serializers.SerializerMethodField(read_only=True)

    class Meta:
        depth = 1
        model = Talent
        fields = (
            'pk',
            'title',
            'view_count',
            'tutor',
            'category',
            'type',
            'tutor_message',
            'location_message',
            'cover_image',
            'tutor_info',
            'class_info',
            'average_rates',
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
    def get_average_rates(obj):
        return AverageRatesSerializer(obj).data


class TalentDetailSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(read_only=True)
    class_images = ClassImageSerializer(many=True, source='classimage_set', read_only=True)
    curriculums = CurriculumSerializer(many=True, source='curriculum_set', read_only=True)
    # reviews = ReviewSerializer(many=True, read_only=True)
    # qna = QuestionSerializer(many=True, source='question_set', read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    average_rates = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    # category = serializers.ChoiceField(choices=Talent.CATEGORY)
    locations = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    reviews = serializers.SerializerMethodField()
    qna = serializers.SerializerMethodField()
    wishlist = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = Talent
        fields = (
            'pk',
            'title',
            'view_count',
            'tutor',
            # 'category_name',
            'tutor_message',
            'category',
            'type',
            'review_count',
            'registration_count',
            'cover_image',
            'tutor_info',
            'class_info',
            'video1',
            'video2',
            'average_rates',
            'location_message',
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
            'qna',
            'reviews',
            'wishlist',
        )
        # '__sizeof__', '__slotnames__', '__str__', '__subclasshook__', '__weakref__', '_add_items', '_apply_rel_filters', '_build_remove_filters', '_constructor_args', '_create_user', '_db', '_get_queryset_methods', '_hints', '_insert', '_queryset_class', '_remove_items', '_set_creation_counter', '_update', 'add', 'aggregate', 'all', 'annotate', 'auto_created', 'bulk_create', 'check', 'clear', 'complex_filter', 'contribute_to_class', 'core_filters', 'count', 'create', 'create_superuser', 'create_user', 'creation_counter', 'dates', 'datetimes', 'db', 'db_manager', 'deconstruct', 'defer', 'distinct', 'do_not_call_in_templates', 'earliest', 'exclude', 'exists', 'extra', 'filter', 'first', 'from_queryset', 'get', 'get_by_natural_key', 'get_or_create', 'get_prefetch_queryset', 'get_queryset', 'in_bulk', 'instance', 'iterator', 'last', 'latest', 'make_random_password', 'model', 'name', 'none', 'normalize_email', 'only', 'order_by', 'prefetch_cache_name', 'prefetch_related', 'query_field_name', 'raw', 'related_val', 'remove', 'reverse', 'select_for_update', 'select_related', 'set', 'source_field', 'source_field_name', 'symmetrical', 'target_field', 'target_field_name', 'through', 'update', 'update_or_create', 'use_in_migrations', 'using', 'values', 'values_list']

    def get_wishlist(self, obj):
        wishlist_users = []
        for wished_user in obj.wishlist_users.all():
            wishlist_users.append(wished_user.user.pk)
        return wishlist_users

    def get_reviews(self, obj):
        ordered_queryset = obj.reviews.order_by('-pk')
        return ReviewSerializer(ordered_queryset, many=True).data

    def get_qna(self, obj):
        ordered_queryset = obj.question_set.order_by('-pk')
        return QuestionSerializer(ordered_queryset, many=True).data

    def get_locations(self, obj):
        regions = {}
        for location_item in obj.locations.all():
            if location_item.region in regions.keys():
                regions[location_item.region] += 1
            else:
                regions[location_item.region] = 1
        locationss = []
        for region_key, value in regions.items():
            a = collections.OrderedDict()
            a["region"] = region_display(region_key)
            a["count"] = value
            results = []
            l = Location.objects.filter(talent=obj, region=region_key)
            for item_l in l:
                results.append(LocationSerializer(item_l).data)
            a["results"] = results
            locationss.append(a)
        return locationss

    def get_category(self, obj):
        return obj.get_category_display()

    @staticmethod
    def get_average_rates(obj):
        return AverageRatesSerializer(obj).data

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
        for index, image in enumerate(self.initial_data.get(
                'c1', validated_data['curriculum_set'])):
            item = Curriculum.objects.filter(talent=instance)[index]
            item.image = image
            # item.image = new_image
            item.save()

        for index, new_curriculum_item in enumerate(validated_data.pop('curriculum_set')):
            new_info = new_curriculum_item["information"]
            # new_image = new_curriculum_item["image"]
            item = Curriculum.objects.filter(talent=instance)[index]
            item.information = new_info
            # item.image = new_image
            item.save()

        return instance


class TalentCreateSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all())

    class Meta:
        model = Talent
        fields = (
            'tutor',
            'title',
            'category',
            'type',
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
            'tutor_message',
            'location_message',
        )


class MyTalentsWrapperSerializer(serializers.ModelSerializer):
    results = TalentShortInfoSerializer(many=True, source="tutor.talent_set")
    user_id = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = (
            'pk',
            'user_id',
            'name',
            'nickname',
            'cellphone',
            'profile_image',
            'joined_date',
            'results',
        )


class TalentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talent
        fields = (
            'title',
            'category',
            'type',
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
            'tutor_message',
        )
