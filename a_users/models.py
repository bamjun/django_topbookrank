from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 기본 필드 (AbstractUser로부터 상속)
    # - username
    # - password
    # - email
    # - first_name
    # - last_name
    # - is_active
    # - is_staff
    # - date_joined

    # 추가 필드
    nickname = models.CharField(max_length=50, unique=True, verbose_name='닉네임')
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True, verbose_name='프로필 이미지')
    phone_number = models.CharField(max_length=11, blank=True, verbose_name='전화번호')
    birth_date = models.DateField(null=True, blank=True, verbose_name='생년월일')

    # 책 관련 추가 필드들
    favorite_categories = models.CharField(max_length=100, blank=True, verbose_name='관심 카테고리')
    favorite_authors = models.CharField(max_length=200, blank=True, verbose_name='선호 작가')
    reading_goal = models.IntegerField(default=0, verbose_name='연간 독서 목표')
    reading_count = models.IntegerField(default=0, verbose_name='올해 읽은 책 수')
    total_reading_count = models.IntegerField(default=0, verbose_name='전체 읽은 책 수')

    # 알림 설정
    notification_settings = models.JSONField(
        default=dict,
        verbose_name='알림 설정',
        help_text='{"price_alert": true, "new_book_alert": true, "review_reminder": true}',
    )

    # 소셜 연동
    social_links = models.JSONField(
        default=dict, verbose_name='소셜 미디어 링크', help_text='{"instagram": "", "facebook": "", "twitter": ""}'
    )

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'

    def __str__(self):
        return self.nickname or self.username


class ReadingStatus(models.Model):
    STATUS_CHOICES = [
        ('reading', '읽는 중'),
        ('completed', '완독'),
        ('want_to_read', '읽고 싶음'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_read')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    review = models.TextField(blank=True)

    class Meta:
        verbose_name = '독서 상태'
        verbose_name_plural = '독서 상태들'
        unique_together = ['user', 'book']


# 독서 통계를 위한 모델
class ReadingStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reading_stats')
    total_pages_read = models.IntegerField(default=0)
    total_reading_time = models.IntegerField(default=0)  # 분 단위
    favorite_genre = models.CharField(max_length=50, blank=True)
    reading_streak = models.IntegerField(default=0)  # 연속 독서일
    last_read_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = '독서 통계'
        verbose_name_plural = '독서 통계들'


# 사용자 활동 기록
class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('review', '리뷰 작성'),
        ('rating', '평점 부여'),
        ('complete', '책 완독'),
        ('start', '책 시작'),
        ('goal_achieve', '목표 달성'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    book = models.ForeignKey('a_books.Book', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    class Meta:
        verbose_name = '사용자 활동'
        verbose_name_plural = '사용자 활동들'
        ordering = ['-created_at']
