from django.db import models


class Book(models.Model):
    """書籍"""
    name = models.CharField('書籍名', max_length=255)
    publisher = models.CharField('出版社', max_length=255, blank=True)
    page = models.IntegerField('ページ数', blank=True, default=0)

    def __str__(self):
        return self.name


class Impression(models.Model):
    """感想"""
    book = models.ForeignKey(Book, verbose_name='書籍', related_name='impressions', on_delete=models.CASCADE)
    comment = models.TextField('コメント', blank=True)

    def __str__(self):
        return self.comment

class Post(models.Model):
    """カード"""
    title = models.CharField('タイトル', max_length=15)
    subtitle = models.CharField('サブタイトル', max_length=15)
    tec_img = models.ImageField(verbose_name='技術の写真', upload_to='images/',)
    desc1 = models.TextField()
    desc2 = models.TextField()
    desc3 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class WorkSeat(models.Model):
    """カード"""
    title = models.CharField('タイトル', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title