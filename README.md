
# DB monitor Database monitoring platform

![](https://img.shields.io/badge/build-release-brightgreen.svg)
![](https://img.shields.io/badge/version-v1.0.0-brightgreen.svg)
![](https://img.shields.io/badge/vue.js-2.9.6-brightgreen.svg)
![](https://img.shields.io/badge/iview-3.4.0-brightgreen.svg?style=flat-square)
![](https://img.shields.io/badge/python-3.6-brightgreen.svg)
![](https://img.shields.io/badge/Django-2.2-brightgreen.svg)

## features
* * - * * building: front end separation architecture, Python Django + + restframework API provides the background, celery custom data acquisition strategy, Iview as a front-end display
UI - * * * * : out of the box front design, high quality offer rich chart, index, core analysis data form trend diagram
- custom * * * * depth: provide complete data monitoring solutions available, farewell long SQL script, commonly used manual, complex data can easily browse through the web page

Introduction to the function of # #

- resource management
- Oracle/MySQL/Redis/Linux resource information input
- resource management as a source of acquisition equipment in all kinds of equipment information, support for dynamic monitoring list join instance
- list of instance
- check each monitor instance list and detailed information
- monitoring alarm
- alarm configuration and alarm information view
- database deployment
- support Oracle19c RAC/RAC One Node/single instance, MySQL5.7/8.0 single instance deployment
    
## The environment

- Python 3.6
    - Django 2.2
    - Django Rest Framework 3.1
    
- Vue.js 2.9
    - iview 3.4

##Platform using
Online access - [] (http://122.51.204.250:8080/), chrome (recommended)

User name: admin
Password: 111111

Note: resources nervous and a variety of reasons, the demo has been discontinued, want to see a classmate to deployment.

Lazy and no contact recommended docker deployment

Docker deployment may refer to:
https://blog.csdn.net/gumengkai/article/details/106250548

Docker (lazy detailed version) deployment can be reference, provide all the installation files, can be used directly in the Intranet:
https://stuxidianeducn-my.sharepoint.com/:f:/g/personal/gumengkai_stu_xidian_edu_cn/EljbazMtQtJKhPKsuY9ZljgBjp7ujQHxPfj6-Hk0dnhyxQ?E = 8 jortk

# # installation deployment
# # # 1. Install python3.6 (abbreviated)

# # # 2. Install mysql5.7 (abbreviated)

Pay attention to the character set: utf-8

The create database db_monitor;

# # # 3. The installation redis3.2 (slightly)

# # # 4. Install oracle instant client (abbreviated)

# # # 5. Project configuration

# # # # download the source code
Git clone https://github.com/gumengkai/db_monitor

# # # # installation depend on the package
PIP install - r requirements. TXT

# # # # configuration Settings
- the MySQL database:

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
		'NAME': 'db_monitor',  
		'USER': 'root',  
		'PASSWORD': 'mysqld',  
        'HOST':'127.0.0.1',  
		'PORT': '3306',  
    }
}

--Redis：

CELERY_RESULT_BACKEND = 'redis: / / localhost: 6379/1'

Redis: / / localhost: 6379/2 CELERY_BROKER_URL = ' '

- email alarm configuration:

IS_SEND_EAMIL = 0 # if send warning E-mail, 0: don't send 1: send

EMAIL_BACKEND = 'django. Core. Mail. Backends. SMTP. EmailBackend' # generally does not need to be modified

EMAIL_HOST = 'smtp.163.com'

EMAIL_PORT = 25

EMAIL_HOST_USER = '* * * * * * * * *' # email login name, such as 11111111111 @163.com

EMAIL_HOST_PASSWORD = '* * * * * * * * *' # the authorization code for the client, not passwords, need to mail service Settings

EMAIL_TO_USER = [' 1782365880 @qq.com ', 'gumengkai@hotmail.com'] # email list, reference format Settings
-- mailing the alarm configuration

IS_SEND_DING_MSG = 0 # if send nailing alarm 0: don't send 1: send

DING_WEBHOOK = '* * * * * * * * * *' # webhook, nailing can get it

# # # # to create the database
python manage.py makemigrations

Python manage. Py migrate

Python manage. Py createsuperuser (create login user)
# # # # to perform database scripts

@ the install/initdata. SQL

Initialization script contains celery initial data and the admin user (password is 111111)

# # # 6. Start/stop
Python manage. Py runserver then executes 0.0.0.0:8000 # suggest using fixed IP address

Celery - A db_monitor worker - l info

Celery - A db_monitor beat - l info

Can also use the startup/shutdown script:

Celery: sh celery_start [shutdown]. Sh

Django: sh web_start [shutdown]. Sh
On the log:

Celery logs: logs/celery - worker. The log & logs/celery - beat. Log

Web log: logs/django - web. Log

Collect data anomalies mainly check the celery log!

Note: if using shell script and stopping time "/ r command not found", for Linux and Windows a newline to difference format, perform under Linux can slip in vim: set ff = Unix is solved

# # # 7. The front-end configuration
Please refer to: [db_monitor_vue] (https://github.com/gumengkai/db_monitor_vue)

# # # 8. Oracle database monitoring
Oracle database monitoring, please set up on the monitored end users, and execute the install/sqlscripts (forOracle) in the script

Grant. & table SQL. SQL & procedure. The SQL

# # # 9. Database deployment
- the Oracle database deployment (support only 19 c version)
If you want to use the function of "database deployment", need to manually download the installation package database and copy to utils/oracle_rac_install/directory.

LINUX. X64_193000_grid_home. Zip, cluster installation, what you don't need to install only a single instance

LINUX. X64_193000_db_home. Zip

Note: before installation need to prepared in advance
1. Yum configuration source
2. Network adapter configuration (rac) installation, including private and public network configuration
3. The server's configuration should be official installation requirements, such as physical memory, disk space, swap, automatic installation program does not check these out
4. Shared disk configuration (rac) installation, need to be done after complete step1 Linux configuration Shared storage configuration, can only continue the follow-up grid installation

5.7/8.0 - MySQL database deployment (support)
Need to manually download the installation package database and copy to utils/mysql_install/directory.
Mysql - 5.7.33 - Linux - glibc2.12 - x86_64. Tar. Gz

Mysql - 8.0.23 - Linux - glibc2.12 - x86_64. Tar. Xz


# # # 10. Access to the address
Depends on his own front-end and back-end port configuration, the default access address is

IP: 8000 / admin -- the back end

IP: 8001 - the front end

# # # 11. System Settings
Such as acquisition frequency, it can be configured in django backstage management page
![not] (images/demo8. JPG)

# # interface display

- asset management

![not] (images/not. JPG)

- an overview of the Oracle database

![not] (images/demo2. JPG)

- top oracle SQL
![not] (images/demo6. JPG)

- the MySQL database log interpretation

![not] (images/demo3. JPG)

- the alarm record

![not] (images/demo4. JPG)

- the alarm configuration

![not] (images/demo5. JPG)

- database deployment

![not] (images/demo7. JPG)

# # exchange of learning
916746047 - the QQ group

In addition, the problems existing in the installation process can look at this document:
https://docs.qq.com/doc/DZHlBSGFGd1lpWUVS

Docker deployment may refer to:
https://blog.csdn.net/gumengkai/article/details/106250548

Copyright © 2019 DB monitor

