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

