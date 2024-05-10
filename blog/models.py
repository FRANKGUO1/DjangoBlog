import logging
from abc import abstractmethod

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField
from uuslug import slugify # 用于管理url

logger = logging.getLogger(__name__)

# Create your models here.
class LinkShowType(models.TextChoices):
    I = ('i', _('index')) # 元组第一个元素是数据库存储的实际值，后一个则是展示给用户的标签
    L = ('l', _('list'))
    P = ('p', _('post'))
    A = ('a', _('all'))
    S = ('s', _('slide'))


# 基础模型类
class BaseModel(models.Model):
    # 继承models.Model类
    id = models.AutoField(primary_key=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('modify time'), default=now)

    # 重写save方法
    def save(self, *args, **kwargs):
        # *args 和 **kwargs 是 Python 中用于处理函数参数的特殊符号，它们的作用是允许函数接受任意数量的位置参数和关键字参数。
        # 位置参数放进元组中，关键字参数则是放进字典中
        # 判断实例是否存在，并判断是否只有views字段更新了
        is_update_views = isinstance(self, Article) and 'update_fields' in kwargs and kwargs['update_fields'] == ['views']
        if is_update_views:
            # 更新浏览数字段,这里的pk是主键
            Article.objects.filter(pk=self.pk).update(views=self.views)
        else:
            # 如果不是，判断slug是否在实例中
            if 'slug' in self.__dict__:
                # self.__dict__ 是一个字典，用于存储实例对象的所有属性和对应的值。
                # 当你创建一个类的实例时，实例对象会有一个名为 __dict__ 的属性，它是一个字典，用于保存实例的所有属性和属性值的映射关系。
                # 如{x:1,y:2}
                slug = getattr(self, 'title') if 'title' in self.__dict__ else getattr(self, 'name')
                setattr(self, 'slug', slugify(slug))
            super().save(*args, **kwargs)

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,path=self.get_absolute_url())
        return url

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass
