from django.conf import settings
from django.db import models
from django.db.models import Model



# Create your models here.
class Goods(models.Model):
    STATUS_CHOICES = [
        ('JD', '京东'),
        ('SN', '苏宁'),
        ('A', '唯品会'),
    ]
    id = models.AutoField(primary_key=True)
    good_id = models.CharField(max_length=30,verbose_name="商品编号")
    good_from = models.CharField(max_length=2,choices=STATUS_CHOICES,verbose_name="数据来源")
    good_title = models.CharField(max_length=200,verbose_name="名称")
    good_link = models.CharField(max_length=200,verbose_name="连接")
    good_img = models.CharField(max_length=200,verbose_name="图片")
    price_queue_id = models.IntegerField(default=0)
    good_price0 = models.CharField(max_length=30,verbose_name="价格0")
    good_price1 = models.CharField(max_length=30,verbose_name="价格1")
    good_price2 = models.CharField(max_length=30,verbose_name="价格2")
    good_price3 = models.CharField(max_length=30,verbose_name="价格3")
    good_price4 = models.CharField(max_length=30,verbose_name="价格4")

    class Meta:
        db_table = 'goods'
        verbose_name = '商品库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.good_title


class Car(models.Model):
    good_id = models.ForeignKey(Goods,on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    class Meta:
        db_table = 'car'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_id