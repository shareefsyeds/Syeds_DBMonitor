from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User
from django.utils import timezone

# Create your models here.

class Users(AbstractUser):
    position = models.CharField(max_length=64, verbose_name='Position information', blank=True, null=True)
    avatar = models.CharField(max_length=256, verbose_name='Head portrait', blank=True, null=True)
    mobile = models.CharField(max_length=11, verbose_name='Mobile phone', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User information'
        verbose_name_plural = verbose_name


class AlertLog(models.Model):

    LOG_LEVEL = [
        ('error', 'error'),
        ('warn', 'warn'),
        ('info', 'info')
    ]

    tags = models.CharField("Label",max_length=32)
    host = models.CharField("Host IP",max_length=32)
    type = models.CharField("Collecting source type 1:The Oracle database 2:The MySQL database 3:Redis 4:Linux",max_length=16)
    log_time = models.CharField("Log time",max_length=255)
    log_level = models.CharField("Level of logging",max_length=16,choices=LOG_LEVEL)
    log_content = models.TextField("Log contents")
    check_time = models.DateTimeField("Acquisition time",default=timezone.now,blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'alert_log'
        verbose_name = "Log analytical data"
        verbose_name_plural = verbose_name

class AlarmConf(models.Model):
    type = models.IntegerField("Collecting source type 1:Oracle database 2:MySQL database 3:Redis 4:Linux")
    name = models.CharField("Alarm name",max_length=128)
    judge = models.CharField("Judge conditions",max_length=8)
    judge_value = models.FloatField("Judgment threshold")
    judge_des = models.CharField("Judge described",max_length=128)
    judge_table = models.CharField("Data source table",max_length=128,blank=True,null=True)
    judge_sql = models.TextField("Determine the SQL")
    conf_table = models.CharField("Configuration table (designed to detect the alarm block)",max_length=128,blank=True,null=True)
    conf_column = models.CharField("Configuration table field (used to test whether the alarm screen)",max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'alarm_conf'
        verbose_name = "The alarm configuration"
        verbose_name_plural = verbose_name

class AlarmInfo(models.Model):
    tags = models.CharField("Label",max_length=32)
    url = models.CharField("Connection address",max_length=255)
    alarm_type = models.CharField("Alarm type",max_length=255)
    alarm_header = models.CharField("Alarm title",max_length=255)
    alarm_content = models.TextField("Alarm title",)
    alarm_time = models.DateTimeField("Alarm time")

    class Meta:
        db_table = 'alarm_info'
        verbose_name = "The alarm information"
        verbose_name_plural = verbose_name

class AlarmInfoHis(models.Model):
    tags = models.CharField("Label",max_length=32)
    url = models.CharField("Connection address",max_length=255)
    alarm_type = models.CharField("Alarm types",max_length=255)
    alarm_header = models.CharField("Alarm title",max_length=255)
    alarm_content = models.TextField("Alarm title",)
    alarm_time = models.DateTimeField("Alarm time")

    class Meta:
        db_table = 'alarm_info_his'
        verbose_name = "The alarm information"
        verbose_name_plural = verbose_name

class SetupLog(models.Model):
    LOG_LEVEL = [
        ('error', 'error'),
        ('warn', 'warn'),
        ('info', 'info')
    ]

    log_type = models.CharField("1:Oracle Rac installation ...",max_length=16)
    log_time = models.CharField("Log time",max_length=255)
    log_level = models.CharField("level of logging",max_length=16,choices=LOG_LEVEL)
    log_content = models.TextField("Log contents")

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'setup_log'
        verbose_name = "Database deployment log"
        verbose_name_plural = verbose_name
