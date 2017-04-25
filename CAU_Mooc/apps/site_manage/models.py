from datetime import datetime


from django.db import models


# index页面轮播图设置表
class Banner(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    image = models.ImageField(verbose_name="轮播图", upload_to="banner/%Y/%m", max_length=100)
    url = models.URLField(verbose_name="访问地址", max_length=200)
    index = models.IntegerField(verbose_name="顺序", default=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
