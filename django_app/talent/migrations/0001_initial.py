from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='talent/extra_images')),
            ],
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('information', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='talent/curriculum')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('KN', '강남'), ('SC', '신촌'), ('SD', '사당'), ('JS', '잠실'), ('JR', '종로'), ('HH', '혜화'), ('YS', '용산'), ('HJ', '합정'), ('MD', '목동'), ('ETC', '기타'), ('KOU', '고려대'), ('SNU', '서울대'), ('YOU', '연세대'), ('HOU', '홍익대'), ('EWWU', '이화여대'), ('BSU', '부산대'), ('JAU', '중앙대'), ('GGU', '건국대'), ('HYU', '한양대')], max_length=4)),
                ('specific_location', models.CharField(choices=[('NEGO', '협의 후 결정'), ('SELF', '직접 입력')], help_text='상세 위치 정보', max_length=4)),
                ('location_info', models.TextField(blank=True)),
                ('extra_fee', models.CharField(choices=[('Y', '예, 있습니다'), ('N', '아니오, 없습니다')], default='N', help_text='장소 및 기타 비용이 있나요?', max_length=1)),
                ('extra_fee_amount', models.CharField(blank=True, help_text='추가 비용: 예시) 재료 비용 1만원', max_length=50)),
                ('day', models.CharField(choices=[('MO', '월'), ('TU', '화'), ('WE', '수'), ('TH', '목'), ('FR', '금'), ('SA', '토'), ('SU', '일')], max_length=2)),
                ('time', models.CharField(help_text=',로 나누어 입력해 주세요. 예시) 13-14시, 18-19시', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('student_level', models.IntegerField(choices=[(1, '입문자'), (2, '초/중급자'), (3, '상급자')], default=1, help_text='레벨 선택')),
                ('experience_length', models.IntegerField(blank=True, default=0, help_text='해당 수업관련 경력을 개월로 입력')),
                ('message_to_tutor', models.TextField(help_text='수강신청시 유저가 튜터에게 보내는 메세지')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to=settings.AUTH_USER_MODEL)),
                ('talent_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='talent.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talent.Question')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Tutor')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('curriculum', models.IntegerField(default=1, help_text='5이하의 숫자를 입력하세요', validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('readiness', models.IntegerField(default=1, help_text='5이하의 숫자를 입력하세요', validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('timeliness', models.IntegerField(default=1, help_text='5이하의 숫자를 입력하세요', validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('delivery', models.IntegerField(default=1, help_text='5이하의 숫자를 입력하세요', validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('friendliness', models.IntegerField(default=1, help_text='5이하의 숫자를 입력하세요', validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Talent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('HNB', '헬스 / 뷰티'), ('LAN', '외국어'), ('COM', '컴퓨터'), ('ART', '미술 / 음악'), ('SPO', '스포츠'), ('JOB', '전공 / 취업'), ('HOB', '이색취미'), ('ETC', '기타')], default='HNB', max_length=3)),
                ('type', models.IntegerField(choices=[(0, '1:1 수업'), (1, '그룹 수업'), (2, '원데이 수업')], default=1)),
                ('cover_image', models.ImageField(upload_to='talent/cover_image')),
                ('tutor_info', models.TextField()),
                ('class_info', models.TextField()),
                ('video1', models.URLField(blank=True)),
                ('video2', models.URLField(blank=True)),
                ('price_per_hour', models.IntegerField(help_text='시간당 가격')),
                ('hours_per_class', models.IntegerField(help_text='기본 수업 시간')),
                ('number_of_class', models.IntegerField(help_text='한달 기준 총 수업 일')),
                ('is_soldout', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('min_number_student', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(1)])),
                ('max_number_student', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(1)])),
                ('tutor_message', models.TextField(blank=True)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Tutor')),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('talent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_users', to='talent.Talent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='talent',
            name='wishlist_user',
            field=models.ManyToManyField(through='talent.WishList', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='talent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='talent.Talent'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='talent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talent.Talent'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='location',
            name='registered_student',
            field=models.ManyToManyField(through='talent.Registration', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='location',
            name='talent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='talent.Talent'),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='talent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talent.Talent'),
        ),
        migrations.AddField(
            model_name='classimage',
            name='talent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talent.Talent'),
        ),
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together=set([('talent', 'user')]),
        ),
    ]
