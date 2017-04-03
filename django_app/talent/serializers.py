from rest_framework import serializers

from member.models import Tutor
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
            # 'talent',
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
    category = serializers.ChoiceField(choices=Talent.CATEGORY, write_only=True)

    class Meta:
        model = Talent
        fields = (
            'tutor_id',
            'tutor_name',
            # 'wishlist_user',
            'class_title',
            'category_name',
            'category',
            'class_image',
            'curriculum',
            'class_type',
            'cover_image',
            'price_per_hour',
            'hours_per_class',
            'number_of_class',
            'is_soldout',
        )

    def get_category_name(self, obj):
        return obj.get_category_display()


class TalentDetailSerializers(serializers.ModelSerializer):
    # tutor_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Tutor.objects.all(), required=True, source='tutor',
    # )
    # tutor_name = serializers.PrimaryKeyRelatedField(read_only=True,
    #                                                 source='tutor.user.name')
    tutor = TutorSerializer(read_only=True)
    class_image = ClassImageSerializers(many=True, source='classimage_set', read_only=False)
    curriculum = CurriculumSerializers(many=True, source='curriculum_set', read_only=False, )
    # curriculum = CurriculumSerializers(many=True, source='curriculum_set', read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    category = serializers.ChoiceField(choices=Talent.CATEGORY)
    location = LocationSerializers(many=True, source='location_set')

    class Meta:
        depth = 2
        model = Talent
        fields = (
            'tutor',
            # 'tutor_id',
            # 'tutor_name',
            # 'wishlist_user',
            'class_title',
            'category',
            'category_name',
            'class_type',
            'cover_image',
            'tutor_info',
            'class_info',
            'video1',
            'video2',
            'location',
            'price_per_hour',
            'hours_per_class',
            'number_of_class',
            'is_soldout',
            'class_image',
            'curriculum',
        )

    def get_category_name(self, obj):
        return obj.get_category_display()

    def update(self, instance, validated_data):
        instance.class_title = validated_data.get('class_title', instance.class_title)
        instance.category = validated_data.get('category', instance.category)
        instance.class_type = validated_data.get('class_type', instance.class_type)
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
