from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

TICKET_PRIORITY = {
    0: '一般',
    1: '紧急',
    2: '非常紧急',
}

STATUS_CHOICES = {
    0: '已提交',
    1: '进行中',
    2: '已结束',
    3: '已拒绝',
}


@python_2_unicode_compatible
class TicketPriority(models.Model):
    """
    工单优先级表
    """
    name = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="优先级名称")

    class Meta:
        verbose_name = '工单优先级'
        verbose_name_plural = '工单优先级'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProductLine(models.Model):
    """
    产品线表
    """
    name = models.CharField(max_length=64, verbose_name='产品线')

    class Meta:
        verbose_name = '产品线'
        verbose_name_plural = '产品线'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AttachMent(models.Model):
    """
    工单附件表
    """
    name = models.FileField(verbose_name='附件')
    ticket = models.ForeignKey(Ticket)

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = '附件'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Ticket(models.Model):
    """
    工单表
    """
    title = models.CharField(max_length=64, verbose_name='工单标题')
    product_line = models.ForeignKey(ProductLine)
    type = models.CharField(max_length=64, verbose_name='分类')
    distribution = models.TextField(verbose_name='工单描述信息')
    create_by = models.ForeignKey(User)
    create_time = models.DateTimeField(default=timezone.now(), verbose_name='工单创建时间')
    update_time = models.DateTimeField(default=timezone.now(), verbose_name='工单更新时间')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='工单状态')
    cc = models.CharField(max_length=255, verbose_name='抄送邮件地址,以分隔')

    class Meta:
        verbose_name = '工单'
        verbose_name_plural = '工单'

    def __str__(self):
        return self.title


class TicketChangedLog(models.Model):
    """
    工单变更信息表
    """
    user = models.ForeignKey(User)
    ticket_id = models.ForeignKey(Ticket)
    # 操作名称,对应调用的方面
    operation = models.CharField(max_length=120, verbose_name='操作')
    # 变更前后的对比信息
    msg = models.TextField(verbose_name='操作信息')
    operation_time = models.TimeField(default=timezone.now(), verbose_name='操作时间')

    class Meta:
        verbose_name = '工单变更信息'
        verbose_name_plural = '工单变更信息'

    def __str__(self):
        return self.msg
