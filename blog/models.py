from email.policy import default
import markdown

from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    # 分类
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    # 标签
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=70)
    # 文章正文
    body = models.TextField('正文')
    # 文章的创建时间和最后一次修改时间
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    # 文章摘要
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 分类与标签
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 文章作者
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    # 新增 views 字段记录阅读量
    views = models.PositiveIntegerField(default=0, editable=False)

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])


    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将 Markdown 文本渲染成 HTML 文本，strip_tags 去掉 HTML 文本的全部 HTML 标签，
        # 从文本中摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:dateil', kwargs={'pk': self.pk})

