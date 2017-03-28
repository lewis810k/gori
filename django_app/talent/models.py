from django.db import models

from member.models import Tutor, GoriUser


class Talent(models.Model):
    CATEGORY = (
        ('HNB', '헬스 / 뷰티'),
        ('LAN', '외국어'),
        ('COM', '컴퓨터'),
        ('ART', '미술 / 음악'),
        ('SPO', '스포츠'),
        ('JOB', '전공 / 취업'),
        ('HOB', '이색취미'),
    )
    CLASS_TYPE_CHOICE = (
        (0, '1:1'),
        (1, '그룹 수업'),
        (2, '원데이 수업'),
    )
    tutor = models.ForeignKey(Tutor, )
    class_title = models.CharField(max_length=30, blank=False)
    category = models.CharField(choices=CATEGORY, max_length=3, blank=False)
    class_type = models.IntegerField(choices=CLASS_TYPE_CHOICE, default=1, blank=False, )
    cover_image = models.ImageField(upload_to='talent/cover_image')
    tutor_info = models.CharField(max_length=80, blank=False)
    class_info = models.CharField(max_length=150, blank=False)
    video1 = models.URLField(blank=True)
    video2 = models.URLField(blank=True)
    price_per_hour = models.IntegerField(blank=False, help_text='시간당 가격')
    hours_per_class = models.IntegerField(blank=False, help_text='기본 수업 시간')
    number_of_class = models.IntegerField(blank=False, help_text='한달 기준 총 수업 일')
    is_soldout = models.BooleanField(default=False)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.class_title)


    def to_dict(self):
        ret = {
            'tutor': self.tutor.to_dict(),
            'class_title': self.class_title,
            'category': self.category,
            'class_type': self.class_type,
            'cover_image': self.cover_image,
            'tutor_info': self.tutor_info,
            'class_info': self.class_info,
            'video1': self.video1,
            'video2': self.video2,
            'price_per_hour': self.price_per_hour,
            'hours_per_class': self.hours_per_class,
            'number_of_class': self.number_of_class,
            'is_soldout': self.is_soldout,

        }
        return ret


class ClassImage(models.Model):
    talent = models.ForeignKey(Talent)
    image = models.ImageField(upload_to='talent/extra_images')


class Registration(models.Model):
    student = models.ForeignKey(GoriUser)
    talent = models.ForeignKey(Talent)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return '{} 님  {}: {} 수업을 신청하였습니다'.format(self.student.name, self.talent.pk, self.talent.class_title)

    def to_dict(self):
        ret = {
            'student':self.student.to_dict(),
            'talent':self.talent.to_dict(),
            'joined_date':self.joined_date.strftime('%Y-%m-%d %H:%M'),
            'is_registered':self.is_registered,
        }
        return ret

class Location(models.Model):
    SCHOOL = (
        ('KOU', '고려대'),
        ('SNU', '서울대'),
        ('YOU', '연세대'),
        ('HOU', '홍익대'),
        ('EWWU', '이화여대'),
        ('BSU', '부산대'),
        ('JAU', '중앙대'),
        ('GGU', '건국대'),
        ('HYU', '한양대'),
        ('SCU', '서울시립대'),
        ('KHU', '경희대'),
        ('SJU', '세종대'),
        ('SGKU', '성균관대'),
        ('GWU', '광운대'),
        ('SMWU', '숙명여대'),
        ('SSWU', '성신여대'),
        ('KMU', '국민대'),
        ('SWU', '서울여대'),
        ('SGU', '서강대'),
        ('MJU', '명지대'),
        ('KIU', '한국외대'),
        ('SSU', '숭실대'),
        ('HYJ', '한예종'),
        ('DGU', '동국대'),
        ('STU', '서울과기대'),
        ('DSWU', '덕성여대'),
        ('SEU', '서울교대'),
        ('DDWU', '동덕여대'),
    )
    AREA = (
        ('KN', '강남'),
        ('SC', '신촌'),
        ('SD', '사당'),
        ('JS', '잠실'),
        ('JR', '종로'),
        ('HH', '혜화'),
        ('YS', '용산'),
        ('HJ', '합정'),
        ('MD', '목동'),
        ('NW', '노원'),
        ('SDR', '신도림'),
        ('YDB', '영등포'),
        ('DDM', '동대문'),
        ('DG', '대구'),
        ('BS', '부산'),
        ('ONL', '온라인'),
    )
    SPECIFIC_LOCATION = (
        ('NEGO', '협의 후 결정'),
        ('SELF', '직접 입력'),
    )
    DAYS_OF_WEEK = (
        ('MO', '월'),
        ('TU', '화'),
        ('WE', '수'),
        ('TH', '목'),
        ('FR', '금'),
        ('SA', '토'),
        ('SU', '일'),
    )
    EXTRA_FEE = (
        ('Y', '예, 있습니다'),
        ('N', '아니오, 없습니다'),
    )
    REGION = AREA + SCHOOL
    talent = models.ForeignKey(Talent, )
    region = models.CharField(choices=REGION, max_length=4)
    specific_location = models.CharField(choices=SPECIFIC_LOCATION, max_length=4, help_text='상세 위치 정보')
    location_info = models.CharField(max_length=10, help_text='직접 입력 10글자 내외', blank=True)
    extra_fee = models.CharField(choices=EXTRA_FEE, max_length=1, default='N', help_text='장소 및 기타 비용이 있나요?')
    extra_fee_amount = models.CharField(max_length=10, help_text='추가 비용: 예시) 재료 비용 1만원', blank=True)
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=2)
    time = models.CharField(max_length=20, help_text=',로 나누어 입력해 주세요. 예시) 13-14시, 18-19시')

    def __str__(self):
        return '{} {}'.format(self.talent, self.region)

class WishList(models.Model):
    talent = models.ForeignKey(Talent,)
    user = models.ForeignKey(GoriUser,)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}의 wishlist에 {} 추가 '.format(self.user.email,self.talent.id)

    def to_dict(self):
        ret = {
            'talent': self.talent.to_dict(),
            'user':self.user.to_dict(),
            'added_date': self.added_date.strftime('%Y-%m-%d %H:%M')
        }
        return ret