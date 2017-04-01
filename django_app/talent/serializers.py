from rest_framework import serializers

from member.models import Tutor, GoriUser
from member.serializers import TutorSerializer
from talent.models import Talent, ClassImage, Curriculum, Location, WishList


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


class TalentListSerializers(serializers.ModelSerializer):
    # tutor_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Tutor.objects.all(), required=True, source='tutor'
    # )
    # tutor_name = serializers.PrimaryKeyRelatedField(read_only=True,
    #                                                 source='tutor.user.name')
    tutor = TutorSerializer()
    category_name = serializers.SerializerMethodField(read_only=True)
    category = serializers.ChoiceField(choices=Talent.CATEGORY, write_only=True)
    class_type_name= serializers.SerializerMethodField(read_only=True)
    class_type = serializers.ChoiceField(choices=Talent.CLASS_TYPE_CHOICE, write_only=True)
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
        )

    def get_category_name(self, obj):
        return obj.get_category_display()

    def get_class_type_name(self, obj):
        return obj.get_class_type_display()


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
