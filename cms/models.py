from django.db import models
from taggit.managers import TaggableManager


#カードモデルの定義
class Card(models.Model):
    """カード"""
    title = models.CharField('技術名称 15文字まで', max_length=15)
    subtitle = models.CharField('サブタイトル 30文字まで', max_length=30, blank=True, null=True)
    tags =  TaggableManager('タグ', blank=True) #タグ付する
    tecimg = models.ImageField(verbose_name='技術の写真', upload_to='images/',) #imagefild->filefildにしたら動画もいけるようになるかも
    tec_desc = models.TextField('機器説明 ',)
    desc1 = models.TextField('具体例1 ',) #必要に応じて追加できるようにしたい
    desc2 = models.TextField('具体例2 ',)
    desc3 = models.TextField('具体例3',)
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    def __str__(self):
        return self.title


#ワークシートモデルの定義
class WorkSeat(models.Model):
    """カード"""
    title = models.CharField('タイトル', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title