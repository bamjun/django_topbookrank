from django.db import models
from django.utils import timezone


class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, verbose_name='ISBN')
    title = models.CharField(max_length=255, verbose_name='책 제목')
    author = models.CharField(max_length=255, verbose_name='저자')
    publisher = models.CharField(max_length=255, verbose_name='출판사')
    publishing = models.DateField(verbose_name='출판일')
    coverurl = models.TextField(verbose_name='표지 이미지 URL')
    category = models.CharField(max_length=20, verbose_name='카테고리')

    class Meta:
        verbose_name = '책'
        verbose_name_plural = '책들'

    def __str__(self):
        return self.title


class KyoboRanking(models.Model):
    rankingid = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='kyobo_ranking', verbose_name='책')
    inputdate = models.DateField(default=timezone.now, verbose_name='입력일')
    kyoborank = models.IntegerField(verbose_name='교보 순위')
    kyoborating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='교보 평점')
    kyoboreview = models.IntegerField(verbose_name='교보 리뷰수')
    kyoboupdown = models.IntegerField(verbose_name='순위 변동')

    class Meta:
        verbose_name = '교보문고 순위 데이터'
        verbose_name_plural = '교보문고 순위 데이터들'
        ordering = ['-inputdate']


class KyoboPrice(models.Model):
    priceid = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='kyobo_price', verbose_name='책')
    inputdate = models.DateField(default=timezone.now, verbose_name='입력일')
    kyoboprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='정가')
    kyobosaleprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='판매가')
    kyobopoint = models.IntegerField(verbose_name='적립 포인트')
    kyobourl = models.TextField(verbose_name='교보문고 URL')

    class Meta:
        verbose_name = '교보문고 가격 데이터'
        verbose_name_plural = '교보문고 가격 데이터들'
        ordering = ['-inputdate']


class Average(models.Model):
    priceid = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='averages', verbose_name='책')
    inputdate = models.DateField(default=timezone.now, verbose_name='입력일')
    averagerating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='평균 평점')
    averageranking = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='평균 순위')
    averageweekranking = models.IntegerField(verbose_name='주간 평균 순위')

    class Meta:
        verbose_name = '평균 데이터'
        verbose_name_plural = '평균 데이터들'
        ordering = ['-inputdate']
