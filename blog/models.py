from django.db import models
from abc import abstractmethod
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.conf import settings
from mdeditor.fields import MDTextField

from uuslug import slugify

from DjangoBlog.utils import get_current_site

# Create your models here.
class LinkShowType(models.TextChoices):
    I = ('i', _('index'))
    L = ('l', _('list'))
    P = ('p', _('post'))
    A = ('a', _('all'))
    S = ('s', _('slide'))


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('modify time'), default=now)

    def save(self, *args, **kwargs):
        is_update_views = isinstance(
            self,
            Article) and 'update_fields' in kwargs and kwargs['update_fields'] == ['views']
        if is_update_views:
            Article.objects.filter(pk=self.pk).update(views=self.views)
        else:
            if 'slug' in self.__dict__:
                slug = getattr(
                    self, 'title') if 'title' in self.__dict__ else getattr(
                    self, 'name')
                setattr(self, 'slug', slugify(slug))
            super().save(*args, **kwargs)

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass

class Article(BaseModel):
    """文章"""
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
    )
    COMMENT_STATUS = (
        ('o', _('Open')),
        ('c', _('Close')),
    )
    TYPE = (
        ('a', _('Article')),
        ('p', _('Page')),
    )
    title = models.CharField(_('title'), max_length=200, unique=True)
    body = MDTextField(_('body'))
    pub_time = models.DateTimeField(
        _('publish time'), blank=False, null=False, default=now)
    status = models.CharField(
        _('status'),
        max_length=1,
        choices=STATUS_CHOICES,
        default='p')
    comment_status = models.CharField(
        _('comment status'),
        max_length=1,
        choices=COMMENT_STATUS,
        default='o')
    type = models.CharField(_('type'), max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField(_('views'), default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    article_order = models.IntegerField(
        _('order'), blank=False, null=False, default=0)
    show_toc = models.BooleanField(_('show toc'), blank=False, null=False, default=False)
    category = models.ForeignKey(
        'Category',
        verbose_name=_('category'),
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    tags = models.ManyToManyField('Tag', verbose_name=_('tag'), blank=True)