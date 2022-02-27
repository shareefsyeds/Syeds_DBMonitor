from django.db import models
# Create your models here.
from django.utils import timezone

class LinuxStat(models.Model):
    tags = models.CharField("Label",max_length=32)
    host = models.CharField("Host IP",max_length=32)
    port = models.IntegerField("SSH port number",default=22)
    hostname = models.CharField("Host name",max_length=64,blank=True,null=True)
    ipinfo = models.CharField("IP address information",max_length=255,blank=True, null=True)
    linux_version = models.CharField("Linux version",max_length=64,blank=True,null=True)
    updays = models.FloatField("Start day",blank=True, null=True)
    kernel = models.CharField("Kernel version",max_length=64,blank=True,null=True)
    frame = models.CharField("System architecture",max_length=64,blank=True,null=True)
    cpu_mode = models.CharField("CPU model",max_length=64,blank=True, null=True)
    cpu_cache = models.CharField("CPU cache",max_length=64,blank=True, null=True)
    processor = models.CharField("Number of CPU core",max_length=64,blank=True, null=True)
    cpu_speed = models.CharField("CPU frequency",max_length=512,blank=True, null=True)
    recv_kbps = models.FloatField("Receives the traffic",blank=True, null=True)
    send_kbps = models.FloatField("Send traffic",blank=True, null=True)
    load1 = models.FloatField(blank=True, null=True)
    load5 = models.FloatField(blank=True, null=True)
    load15 = models.FloatField(blank=True, null=True)
    cpu_sys = models.FloatField(blank=True, null=True)
    cpu_iowait = models.FloatField(blank=True, null=True)
    cpu_user = models.FloatField(blank=True, null=True)
    cpu_used = models.FloatField("CPU usage",blank=True, null=True)
    memtotal = models.FloatField("Total memory size",blank=True, null=True)
    mem_used = models.FloatField("Memory usage",blank=True, null=True)
    mem_cache = models.FloatField(blank=True, null=True)
    mem_buffer = models.FloatField(blank=True, null=True)
    mem_free = models.FloatField(blank=True, null=True)
    mem_used_mb = models.FloatField(blank=True, null=True)
    swap_used = models.FloatField(blank=True, null=True)
    swap_free = models.FloatField(blank=True, null=True)
    swapin = models.FloatField(blank=True, null=True)
    swapout = models.FloatField(blank=True, null=True)
    pgin = models.FloatField(blank=True, null=True)
    pgout = models.FloatField(blank=True, null=True)
    pgfault = models.FloatField(blank=True, null=True)
    pgmjfault = models.FloatField(blank=True, null=True)
    tcp_close = models.FloatField(blank=True, null=True)
    tcp_timewait = models.FloatField(blank=True, null=True)
    tcp_connected = models.FloatField(blank=True, null=True)
    tcp_syn = models.FloatField(blank=True, null=True)
    tcp_listen = models.FloatField(blank=True, null=True)
    iops = models.FloatField(blank=True, null=True)
    read_mb = models.FloatField(blank=True, null=True)
    write_mb = models.FloatField(blank=True, null=True)
    proc_new = models.FloatField(blank=True, null=True)
    proc_running = models.FloatField(blank=True, null=True)
    proc_block = models.FloatField(blank=True, null=True)
    intr = models.FloatField(blank=True, null=True)
    ctx = models.FloatField(blank=True, null=True)
    softirq = models.FloatField(blank=True, null=True)
    status = models.IntegerField("Linux host connection status 0 success 1 Failure",blank=True, null=True)
    check_time = models.DateTimeField("Acquisition time",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_stat'
        verbose_name = "Linux host to collect data"
        verbose_name_plural = verbose_name


class LinuxDisk(models.Model):
    tags = models.CharField("Label",max_length=32)
    host = models.CharField("Host IP",max_length=32)
    dev = models.CharField("Equipment",max_length=64,blank=True,null=True)
    total_size = models.FloatField("Total size",blank=True, null=True)
    used_size = models.FloatField("Used space size",blank=True, null=True)
    free_size = models.FloatField("Remaining space size",blank=True,null=True)
    used_percent = models.FloatField("usage",blank=True,null=True)
    mount_point = models.CharField("Mount point",max_length=256,blank=True,null=True)
    check_time = models.DateTimeField("Acquisition time",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_disk'
        verbose_name = "Linux disk information acquisition data"
        verbose_name_plural = verbose_name

class LinuxIoStat(models.Model):
    tags = models.CharField("Label",max_length=32)
    host = models.CharField("Host IP",max_length=32)
    dev = models.CharField("Equipment",max_length=64,blank=True,null=True)
    rd_s = models.FloatField("Read requests per second",blank=True, null=True)
    rd_avgkb = models.FloatField("Read requests an average size",blank=True, null=True)
    rd_m_s = models.FloatField("Read size (MB) per second",blank=True, null=True)
    rd_mrg_s = models.FloatField("Read per second merge (percentage)",blank=True, null=True)
    rd_cnc = models.FloatField("Read the concurrency",blank=True, null=True)
    rd_rt = models.FloatField("Read the response time",blank=True, null=True)
    wr_s = models.FloatField("Write requests per second",blank=True, null=True)
    wr_avgkb = models.FloatField("Write requests an average size",blank=True, null=True)
    wr_m_s = models.FloatField("Write size (MB) per second",blank=True, null=True)
    wr_mrg_s = models.FloatField("Write a second merge (percentage)",blank=True, null=True)
    wr_cnc = models.FloatField("Write the number of concurrent",blank=True, null=True)
    wr_rt = models.FloatField("Write the corresponding time",blank=True, null=True)
    busy = models.FloatField("%util",blank=True, null=True)
    in_prg = models.FloatField("Queued requests",blank=True, null=True)
    io_s = models.FloatField("Physical disk throughput",blank=True, null=True)
    qtime = models.FloatField("IO request queue time (average queue time)",blank=True, null=True)
    stime = models.FloatField("IO request service time",blank=True, null=True)
    check_time = models.DateTimeField("Acquisition time",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_io_stat'
        verbose_name = "Linux disk I/o information"
        verbose_name_plural = verbose_name


class LinuxStatHis(models.Model):
    tags = models.CharField("Label",max_length=32)
    host = models.CharField("Host IP",max_length=32)
    port = models.IntegerField("SSH port number",default=22)
    hostname = models.CharField("Host name.",max_length=64,blank=True,null=True)
    ipinfo = models.CharField("IP address information",max_length=255,blank=True, null=True)
    linux_version = models.CharField("Linux version",max_length=64,blank=True,null=True)
    updays = models.FloatField("Start day",blank=True, null=True)
    kernel = models.CharField("Kernel version",max_length=64,blank=True,null=True)
    frame = models.CharField("System architecture",max_length=64,blank=True,null=True)
    cpu_mode = models.CharField("CPU model",max_length=64,blank=True, null=True)
    cpu_cache = models.CharField("CPU cache",max_length=64,blank=True, null=True)
    processor = models.CharField("Number of CPU core",max_length=64,blank=True, null=True)
    cpu_speed = models.CharField("CPU frequency",max_length=512,blank=True, null=True)
    recv_kbps = models.FloatField("Receives the traffic",blank=True, null=True)
    send_kbps = models.FloatField("Send traffic",blank=True, null=True)
    load1 = models.FloatField(blank=True, null=True)
    load5 = models.FloatField(blank=True, null=True)
    load15 = models.FloatField(blank=True, null=True)
    cpu_sys = models.FloatField(blank=True, null=True)
    cpu_iowait = models.FloatField(blank=True, null=True)
    cpu_user = models.FloatField(blank=True, null=True)
    cpu_used = models.FloatField("CPU usage",blank=True, null=True)
    memtotal = models.FloatField("Total memory size",blank=True, null=True)
    mem_used = models.FloatField("Memory usage",blank=True, null=True)
    mem_cache = models.FloatField(blank=True, null=True)
    mem_buffer = models.FloatField(blank=True, null=True)
    mem_free = models.FloatField(blank=True, null=True)
    mem_used_mb = models.FloatField(blank=True, null=True)
    swap_used = models.FloatField(blank=True, null=True)
    swap_free = models.FloatField(blank=True, null=True)
    swapin = models.FloatField(blank=True, null=True)
    swapout = models.FloatField(blank=True, null=True)
    pgin = models.FloatField(blank=True, null=True)
    pgout = models.FloatField(blank=True, null=True)
    pgfault = models.FloatField(blank=True, null=True)
    pgmjfault = models.FloatField(blank=True, null=True)
    tcp_close = models.FloatField(blank=True, null=True)
    tcp_timewait = models.FloatField(blank=True, null=True)
    tcp_connected = models.FloatField(blank=True, null=True)
    tcp_syn = models.FloatField(blank=True, null=True)
    tcp_listen = models.FloatField(blank=True, null=True)
    iops = models.FloatField(blank=True, null=True)
    read_mb = models.FloatField(blank=True, null=True)
    write_mb = models.FloatField(blank=True, null=True)
    proc_new = models.FloatField(blank=True, null=True)
    proc_running = models.FloatField(blank=True, null=True)
    proc_block = models.FloatField(blank=True, null=True)
    intr = models.FloatField(blank=True, null=True)
    ctx = models.FloatField(blank=True, null=True)
    softirq = models.FloatField(blank=True, null=True)
    status = models.IntegerField("Linux host connection state 0 success 1 failed",blank=True, null=True)
    check_time = models.DateTimeField("Acquisition time",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_stat_his'
        verbose_name = "Linux host data."
        verbose_name_plural = verbose_name


class LinuxDiskHis(models.Model):
    tags = models.CharField("Label",max_length=32)
    host = models.CharField("Host IP",max_length=32)
    dev = models.CharField("Equipment",max_length=64,blank=True,null=True)
    total_size = models.FloatField("Total size",blank=True, null=True)
    used_size = models.FloatField("Used space",blank=True, null=True)
    free_size = models.FloatField("Remaining space size",blank=True,null=True)
    used_percent = models.FloatField("Usage",blank=True,null=True)
    mount_point = models.CharField("Mount point",max_length=256,blank=True,null=True)
    check_time = models.DateTimeField("Acquisition time",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_disk_his'
        verbose_name = "LinuX disk information acquisition data"
        verbose_name_plural = verbose_name

class LinuxIoStatHis(models.Model):
    tags = models.CharField("Label",max_length=32)
    host = models.CharField("Host IP",max_length=32)
    dev = models.CharField("Equipment",max_length=64,blank=True,null=True)
    rd_s = models.FloatField("Read requests per second",blank=True, null=True)
    rd_avgkb = models.FloatField("Read requests an average size",blank=True, null=True)
    rd_m_s = models.FloatField("Read size (MB) per second",blank=True, null=True)
    rd_mrg_s = models.FloatField("Second read merger (%)",blank=True, null=True)
    rd_cnc = models.FloatField("Read concurrency",blank=True, null=True)
    rd_rt = models.FloatField("Read response time",blank=True, null=True)
    wr_s = models.FloatField("Write requests per second",blank=True, null=True)
    wr_avgkb = models.FloatField("Write requests an average size",blank=True, null=True)
    wr_m_s = models.FloatField("Write size (MB) per second",blank=True, null=True)
    wr_mrg_s = models.FloatField("Write a second merge (percentage)",blank=True, null=True)
    wr_cnc = models.FloatField("Write the number of concurrent",blank=True, null=True)
    wr_rt = models.FloatField("Write the corresponding time",blank=True, null=True)
    busy = models.FloatField("%util",blank=True, null=True)
    in_prg = models.FloatField("Queued requests",blank=True, null=True)
    io_s = models.FloatField("Physical disk throughput",blank=True, null=True)
    qtime = models.FloatField("IO request queue time (average queuing time)",blank=True, null=True)
    stime = models.FloatField("IO request service time",blank=True, null=True)
    check_time = models.DateTimeField("Acquisition time",default=timezone.now,blank=True,null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'linux_io_stat_his'
        verbose_name = "Linux disk IO information"
        verbose_name_plural = verbose_name
