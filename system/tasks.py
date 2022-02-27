from celery import shared_task
from check.maincheck import checkall
from utils.oracle_rac_install import OracleRacInstall
from utils.oracle_rac_onenode_install import OracleRacOneNodeInstall
from utils.oracle_onenode_install import OracleOneNodeInstall
from utils.mysql_install import MysqlInstall


@shared_task
def main_check():
    checkall()
    return

@shared_task
def oracle_rac_setup(rac_info,node_list,module):
    print('Oracle RAC installation is started！')
    oracle_rac_install = OracleRacInstall(rac_info, node_list)
    oracle_rac_install.do_rac_install(module)

@shared_task
def oracle_rac_onenode_setup(node_info,module):
    print('Oracle RAC One Node installation is started！')
    oracle_rac_onenode_install = OracleRacOneNodeInstall(node_info)
    oracle_rac_onenode_install.do_rac_install(module)

@shared_task
def oracle_onenode_setup(node_info,module):
    print('Oracle One Node installation is started！')
    oracle_onenode_install = OracleOneNodeInstall(node_info)
    oracle_onenode_install.do_onenode_install(module)


@shared_task
def mysql_setup(node_info):
    print('MySQL installation is started！')
    mysql_install = MysqlInstall(node_info)
    mysql_install.do_mysql_install()