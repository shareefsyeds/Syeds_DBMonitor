# encoding:utf-8
from django.db import models

# Create your models here.

# oracle Monitor the list
class OracleList(models.Model):

    DB_VERSION = [
        ('Oracle11g','Oracle11g'),
        ('Oracle12c', 'Oracle12c'),
        ('Oracle19c', 'Oracle19c'),
    ]

    ALARM_CHOICES = [
        (0,'enable '),
        (1,'disable')
    ]

    tags = models.CharField("Label",max_length=32,unique=True)
    host = models.CharField("Host ip",max_length=32)
    port = models.IntegerField("Database port number",default=1521)
    service_name = models.CharField("Database service name",max_length=255)
    db_version = models.CharField("Database version",max_length=32,choices=DB_VERSION)
    dbname = models.CharField("Database name",max_length=255,blank=True,null=True)
    instance_name = models.CharField("Instance name",max_length=255,blank=True,null=True)
    db_vip = models.CharField("VIP address",max_length=255,blank=True,null=True)
    db_loc = models.CharField("Installation address",max_length=255,blank=True,null=True)
    bussiness_system = models.CharField("Business system",max_length=255,blank=True,null=True)
    system_level = models.IntegerField("System level 0:Core system 1:Important systems 2:一System",default=0)
    res_description = models.CharField("Resource description",max_length=255,blank=True,null=True)
    main_dbuser = models.CharField("Primary use户",max_length=255,blank=True,null=True)
    db_user = models.CharField("Database user name",max_length=32)
    db_password = models.CharField("Database user password",max_length=255)
    service_name_cdb = models.CharField("Database service name(cdb)", max_length=255, blank=True,null=True)
    db_user_cdb = models.CharField("Database user name(cdb)", max_length=32, blank=True,null=True)
    db_password_cdb = models.CharField("Database user password(cdb) ", max_length=255, blank=True,null=True)
    linux_tags = models.CharField("Linux host tag",max_length=32,blank=True,null=True)
    alarm_connect = models.IntegerField("On and off the alarm",default=1)
    alarm_tablespace = models.IntegerField("Tablespace warning",default=1)
    alarm_undo_tablespace = models.IntegerField("Undo tablespace warning",default=1)
    alarm_temp_tablespace = models.IntegerField("Temp tablespace warning",default=1)
    alarm_process = models.IntegerField("Nnumber of connections the alarm",default=1)
    alarm_pga = models.IntegerField("Pga alarm",default=1)
    alarm_archive = models.IntegerField("Archive utilization warning",default=1)
    alarm_adg = models.IntegerField("adg delay alarm",default=1)
    alarm_alert_log = models.IntegerField("Background log alarms",default=1)
    alarm_lock = models.IntegerField("Lock faults",default=1)
    alarm_invalid_index = models.IntegerField("Index of failure alarm",default=1)
    alarm_expired_password = models.IntegerField("Password expired alarms",default=1)
    alarm_wait_events = models.IntegerField("Comprehensive performance warning",default=1)
    alert_log = models.CharField("Background log path",max_length=256,blank=True,null=True)
    alert_log_seek = models.IntegerField("Backstage log offset",blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'oracle_list'
        verbose_name = "Oracle database"
        verbose_name_plural = verbose_name

# mysql Monitor the list
class MysqlList(models.Model):

    DB_VERSION = [
        ('MySQL5.6','MySQL5.6'),
        ('MySQL5.7', 'MySQL5.7'),
        ('MySQL8.0', 'MySQL8.0')
    ]
    ALARM_CHOICES = [
        (0,'enable'),
        (1,'disable')
    ]

    ISON = [
        (0,'ON'),
        (1,'OFF')
    ]

    tags = models.CharField("Label",max_length=32,unique=True)
    host = models.CharField("Host IP",max_length=32)
    port = models.IntegerField("Database port number",default=3306)
    db_version = models.CharField("Database version",max_length=32,choices=DB_VERSION)
    db_user = models.CharField("Database user name", max_length=32)
    db_password = models.CharField("Database user password", max_length=255)
    linux_tags = models.CharField("Linux host tag",max_length=32,blank=True,null=True)
    vip = models.CharField("Virtual IP address",max_length=32,blank=True, null=True)
    db_role = models.CharField("Database roles", max_length=32, blank=True, null=True)
    readonly = models.CharField("Read-only", max_length=32, choices=ISON, blank=True, null=True)
    gtid = models.CharField("Gtid whether to enable",max_length=32,choices=ISON,blank=True, null=True)
    start_method = models.CharField("Start the way", max_length=100, blank=True, null=True)
    datadir = models.CharField("Data directory", max_length=32, blank=True, null=True)
    appdir = models.CharField("Application directory", max_length=32, blank=True, null=True)
    profile = models.CharField("Configuration file", max_length=32, blank=True, null=True)
    backup_type = models.CharField("Backups",max_length=32,blank=True, null=True)
    architecture = models.CharField("Architecture (high availability)",max_length=32,blank=True, null=True)
    bussiness_system = models.CharField("Business system", max_length=255, blank=True, null=True)
    system_level = models.IntegerField("System level 0:Core system 1:Important systems 2:一System", default=0)
    res_description = models.CharField("Resource description", max_length=255, blank=True, null=True)
    main_dbuser = models.CharField("Primary user", max_length=255, blank=True, null=True)
    alarm_connect = models.IntegerField("On and off the alarm",default=1)
    alarm_repl = models.IntegerField("Replication delay alarm",default=1)
    alarm_connections = models.IntegerField("Number of connections the alarm",default=1)
    alarm_alert_log = models.IntegerField("Background log alarms",default=1)
    alert_log = models.CharField("Background the log file",max_length=256,blank=True,null=True)
    alert_log_seek = models.IntegerField("Background log file offset",blank=True,null=True)
    slowquery_log = models.CharField("Slow query log file",max_length=256,blank=True,null=True)
    slowquery_log_seek = models.IntegerField("Slow query log file offset",blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'mysql_list'
        verbose_name = "MySQL Database"
        verbose_name_plural = verbose_name

# linx monitoring list
class LinuxList(models.Model):

    LINUX_VERSION = [
        ('Linux6','Linux6'),
        ('Linux7', 'Linux7'),
    ]

    ALARM_CHOICES = [
        (0,'enable'),
        (1,'disable')
    ]

    STATUS = [
        (0, 'online'),
        (1, 'The standby'),
        (2, 'offline'),
        (3, 'Stay with'),
        (4, 'maintenance'),
        (5, 'reinstall')    ]

    tags = models.CharField("Label",max_length=32,unique=True)
    host = models.CharField("Host IP",max_length=32)
    hostname = models.CharField("Host name",max_length=256)
    linux_version = models.CharField("Linux version",max_length=32,choices=LINUX_VERSION)
    linux_kernel = models.CharField("Kernel version",max_length=64,blank=True,null=True)
    user = models.CharField("Host user name",max_length=32)
    password = models.CharField("Host user password",max_length=255)
    sshport = models.IntegerField("Host SSH port",default=22)
    serialno = models.CharField("Serial number",max_length=100,blank=True,null=True)
    status = models.IntegerField("State",choices=STATUS,blank=True,null=True)
    cabinet = models.CharField("Cabinet",max_length=100,blank=True,null=True)
    factory = models.CharField("Server manufacturer",max_length=100,blank=True,null=True)
    purchase_date = models.CharField("Date of purchase",max_length=32,blank=True,null=True)
    beginprotection_date = models.CharField("Warranty start date",max_length=32,blank=True,null=True)
    overprotection_date = models.CharField("Confirmed date",max_length=32,blank=True,null=True)
    bussiness_system = models.CharField("Business system",max_length=255,blank=True,null=True)
    system_level = models.IntegerField("System level 0:Core system 1:Important systems 2:一System",default=0)
    res_description = models.CharField("Resource description",max_length=255,blank=True,null=True)
    main_software = models.CharField("Main software deployment",max_length=255,blank=True,null=True)
    alarm_connect = models.IntegerField("On and off the alarm",default=1)
    alarm_cpu = models.IntegerField("Warning CPU utilization",default=1)
    alarm_mem = models.IntegerField("Memory usage warning",default=1)
    alarm_swap = models.IntegerField("Swap usage warning",default=1)
    alarm_disk = models.IntegerField("Disk usage warning",default=1)
    alarm_alert_log = models.IntegerField("Background log alarms",default=1)
    alert_log = models.CharField("Backstage log path",max_length=256,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_list'
        verbose_name = "LinuxThe host"
        verbose_name_plural = verbose_name

# Redis monitoring list
class RedisList(models.Model):

    REDIS_VERSION = [
        ('Redis3','Redis3')
    ]

    ALARM_CHOICES = [
        (0,'enable'),
        (1,'disable')
    ]

    ROLE_CHOICES = [
        ('master','master'),
        ('slave','slave')
    ]

    tags = models.CharField("Label",max_length=32,unique=True)
    host = models.CharField("Host IP",max_length=32)
    port = models.IntegerField("Database port number",default=6379)
    password = models.CharField("Password",max_length=255,blank=True,null=True)
    linux_tags = models.CharField("Linux host tag",max_length=32,blank=True,null=True)
    redis_version = models.CharField("Redis version",max_length=32,choices=REDIS_VERSION,blank=True,null=True)
    role = models.CharField("Role",max_length=32,choices=ROLE_CHOICES,blank=True,null=True)
    appdir = models.CharField("Application directory",max_length=128,blank=True,null=True)
    profile = models.CharField("Configuration file",max_length=256,blank=True,null=True)
    architecture = models.CharField("Architecture (high availability)", max_length=32, blank=True, null=True)
    bussiness_system = models.CharField("Business system", max_length=255, blank=True, null=True)
    system_level = models.IntegerField("System level 0:Core system 1:Important systems 2:一System", default=0)
    res_description = models.CharField("Resource description", max_length=255, blank=True, null=True)
    alarm_connect = models.IntegerField("On and off the alarm",default=1)
    alarm_alert_log = models.IntegerField("Background log alarms",default=1)
    log = models.CharField("Background log path",max_length=256,blank=True,null=True)
    log_seek = models.IntegerField("Background log file offset",blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'redis_list'
        verbose_name = "Redis"
        verbose_name_plural = verbose_name
