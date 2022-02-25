# encoding： utf-8

from utils.linux_base import LinuxBase
from utils.tools import now_local
from utils.tools import mysql_exec,mysql_query,now,get_memtotal
import os

class OracleOneNodeInstall():
    def __init__(self, node_info):
        self.node_info = node_info
        self.linux_group_list = [
            [501, 'dba'],
            [502, 'oinstall'],
            [503, 'oper']
        ]
        self.linux_user_list = {
            'oracle': 501
        }
        self.linux_packages = "openssh bc binutils compat-libcap1 compat-libstdc++ elfutils-libelf elfutils-libelf-devel fontconfig-devel glibc " \
                              "glibc-devel ksh libaio libaio-devel libX11 libXau libXi libXtst libXrender libXrender-devel libgcc librdmacm-devel " \
                              "libstdc++ libstdc++-devel libxcb make smartmontools sysstat gcc-c++ nfs-utils net-tools unzip expect"

        self.local_path = os.getcwd() + '/utils/oracle_rac_install/'


    def clear_log(self):
        sql = 'truncate table setup_log'
        mysql_exec(sql,)

    def log(self,log_content):
        log_level = 'info'
        log_type = 'Oracle One Node The installation'
        current_time = now_local()
        print('{}: {}'.format(current_time,log_content))
        sql = "insert into setup_log(log_type,log_time,log_level,log_content)" \
              "values(%s,%s,%s,%s)"
        values = (log_type,current_time,log_level,log_content)
        mysql_exec(sql, values)

    def clear_rac(self):
        self.log('Began to clean up Oracle RAC')
        # Delete the directory
        cmd_list = [
            'rm -rf /u01',
            'rm -f /usr/local/bin/dbhome',
            'rm -f /usr/local/bin/oraenv',
            'rm -f /usr/local/bin/coraenv',
            'rm -f /etc/oratab',
            'rm -f /etc/oraInst.loc',
            'rm -rf /etc/oracle',
            'rm -rf /etc/ora*',
            'rm -rf /etc/init/oracle*',
            'rm -rf /etc/init.ohasd',
            'rm -rf /etc/ohasd',
            'rm -rf /etc/init.tfa',
            'rm -rf /var/tmp/.oracle',
            'rm -rf /tmp/CVU*',
            'rm -rf /tmp/OraInstall*',
            'rm -rf /var/tmp/.oracle',
            'rm -rf /opt/oracle'
        ]
        # Delete the user group
        cmd_list.extend(
            ['groupdel {}'.format(group[1]) for group in self.linux_group_list]
        )
        # Delete user
        cmd_list.extend(
            ['userdel -rf oracle'],
        )
        # Clean up after the completion of the restart the server
        cmd_list.extend(
            ['reboot']
        )
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['node_password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        self.log('{}：Began to clean up Oracle RAC！'.format(self.node_info['node_ip']))
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('Oracle RAC Clean up the complete！')


    def upload_software(self, linux_params):
        # File upload
        LinuxBase(linux_params).sftp_upload_file('{}oracle_profile'.format(self.local_path), '/tmp/oracle_profile')
        LinuxBase(linux_params).sftp_upload_file('{}compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm'.format(self.local_path),
                                                 '/tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm')
        LinuxBase(linux_params).sftp_upload_file('{}97-oracle-database-sysctl.conf'.format(self.local_path),
                                                 '/tmp/97-oracle-database-sysctl.conf')
        LinuxBase(linux_params).sftp_upload_file('{}oracle-database-preinstall-19c.conf'.format(os.getcwd() + '/utils/oracle_onenode_install/'),
                                                 '/tmp/oracle-database-preinstall-19c.conf')
    
    def get_shm_config(self):
        memtotal = get_memtotal(self.node_info['node_ip'],self.node_info['node_password'])
        # Physical memory 1g unit for bytes
        shmmax = (float(memtotal)/1024/1024-1)*1024*1024*1024
        # Physical memory 1g unit for the page
        shmall = (float(memtotal)/1024/1024-1)*1024*1024/4
        return (int(shmmax),int(shmall))

    def linux_config(self):
        cmd_list = []

        # Modify /etc/hosts
        ip_conf = "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n" \
                  "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6\n" \
                  "{}  {}\n".format(self.node_info['node_ip'], self.node_info['hostname'])
        cmd_list.extend([
            'cat /dev/null > /etc/hosts',
            'echo "{}" > /etc/hosts'.format(ip_conf)
        ])
        # To disable the firewall
        cmd_list.extend([
            'systemctl stop firewalld',
            'systemctl disable firewalld',
            "sed -i 's/SELINUX=enabled/SELINUX=disabled/g' /etc/selinux/config "
        ])
        # Disable the NTP service

        # Create a group, and the user
        group_list = ['groupdel {}'.format(group[1]) for group in self.linux_group_list] + \
                     ['groupadd -g {} {}'.format(group[0], group[1]) for group in self.linux_group_list]
        cmd_list.extend(group_list)
        cmd_list.extend([
            'userdel -rf oracle',
            'useradd -u {} -g oinstall -G dba,oper oracle'.format(
                self.linux_user_list['oracle']),
            "echo 'oracle:oracle'|chpasswd"
        ])

        # Create a directory, authorization
        cmd_list.extend([
            'rm -rf /u01',
            'mkdir -p /u01/app/oracle/product/19.0.0/dbhome_1/',
            'mkdir -p /u01/app/oraInventory',
            'chown -R oracle:oinstall /u01/app/oracle',
            'chown -R oracle:oinstall /u01/app/oraInventory',
            'chmod -R 775 /u01/'
        ])

        # Yum install the necessary packages
        cmd_list.extend([
            'yum -y install {}'.format(self.linux_packages),
            'rpm -ivh /tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm'
        ])

        # The kernel parameter Settings
        shmmax,shmall = self.get_shm_config()
        cmd_list.extend([
            'mv /tmp/97-oracle-database-sysctl.conf /etc/sysctl.d/97-oracle-database-sysctl.conf',
            "sed -i 's/NODE_SHMMAX/{}/g' /etc/sysctl.d/97-oracle-database-sysctl.conf".format(shmmax),
            "sed -i 's/NODE_SHMALL/{}/g' /etc/sysctl.d/97-oracle-database-sysctl.conf".format(shmall),
            '/sbin/sysctl --system',
            '/sbin/sysctl -a'
        ])
        # Resource limits set
        cmd_list.extend([
            'mv /tmp/oracle-database-preinstall-19c.conf /etc/security/limits.d/oracle-database-preinstall-19c.conf'
        ])

        # Perform runfixup script
        # cmd_list.extend([
        #     'sh /tmp/runfixup.sh'
        # ])

        return cmd_list

    def do_linux_config(self):
        self.log('Configure Linux foundation started..')
        self.log('{} {}：To begin the Linux operating system configuration！'.format(self.node_info['node_ip'], self.node_info['hostname']))
        cmd_list = self.linux_config()

        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['node_password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()

        self.upload_software(linux_params)

        # To modify the hostname
        cmd_list.extend([
            'hostnamectl set-hostname {}'.format(self.node_info['hostname'])
        ])

        # Modify the profile file (individually)
        cmd_list.extend([
            'mv /tmp/oracle_profile /home/oracle/.bash_profile',
            'chown oracle:oinstall /home/oracle/.bash_profile',
            "sed -i 's/NODE_ORACLE_SID/{}/g' /home/oracle/.bash_profile".format(
                self.node_info['dbname'])
        ])

        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('{} {}：linux The operating system configuration is complete'.format(self.node_info['node_ip'], self.node_info['hostname']))

        self.log('linux Basic configuration is complete！')

    def oracle_execute_scripts(self):
        cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/root.sh'
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['node_password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        LinuxBase(linux_params).exec_command_res(cmd)

    def oracle_install(self):
        self.log('Begin the oracle software installation..')
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'oracle',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        self.log('{} {}：Began to upload the oracle installation package..'.format(self.node_info['node_ip'], self.node_info['hostname']))
        LinuxBase(linux_params).sftp_upload_file('{}LINUX.X64_193000_db_home.zip'.format(self.local_path),'/tmp/LINUX.X64_193000_db_home.zip')
        self.log('oracle installation package to upload to complete！')
        self.log('Started to unzip the oracle installation package..')
        cmd = 'unzip -q -o /tmp/LINUX.X64_193000_db_home.zip -d /u01/app/oracle/product/19.0.0/dbhome_1/'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('oracle installation package decompression！')
        cmd = 'rm -f /tmp/LINUX.X64_193000_db_home.zip'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('Oracle installer clean finish！')

        self.log('Begin to generate oracle install response file..')
        LinuxBase(linux_params).sftp_upload_file('{}db_install_onenode.rsp'.format(os.getcwd() + '/utils/oracle_onenode_install/'), '/tmp/db_install.rsp')
        self.log('The oracle install response cannot be completed！')

        self.log('Before installing the oracle software configuration is successful, please in the node{}Use of oracle users perform silent installation script：'
                 '/u01/app/oracle/product/19.0.0/dbhome_1/runInstaller -silent -ignorePrereqFailure -responsefile /tmp/db_install.rsp '
                 ' And according to the prompt follow-up script execution'.format(self.node_info['node_ip']))

        # silent installation
        # the self. The log (' start Oracle software silent installation, pay attention to {} : / TMP/oraclesetup log '. The format (node (IP)))
        # CMD = '/ u01 / app/oracle/product / 19.0.0 / dbhome_1 / runInstaller - silent - ignorePrereqFailure - responsefile/TMP/db_install RSP > / TMP/oraclesetup log'
        # LinuxBase (linux_params). Exec_command_res (CMD)
        # self. The log (' silent Oracle software installation is complete!')
        # the self. The log (' according to the/TMP/oraclesetup. Please log in the tip executing scripts!')

        # 执行root脚本
        # self.oracle_execute_scripts()

    def oracle_dbca(self):
        self.log('To begin building library dbca..')

        oracle_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'oracle',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(oracle_params).connection()

        self.log('To start generating dbca building response file..')
        LinuxBase(oracle_params).sftp_upload_file('{}dbca_onenode.rsp'.format(os.getcwd() + '/utils/oracle_onenode_install/'), '/tmp/dbca.rsp')

        # Modify the response file
        cmd_list = [
            "sed -i 's/NODE_DBNAME/{}/g' /tmp/dbca.rsp".format(self.node_info['dbname']),
            "sed -i 's/NODE_PDBNAME/{}/g' /tmp/dbca.rsp".format(self.node_info['pdbname'])
        ]
        res = [LinuxBase(oracle_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('dbca建库响应文件生成完成！')

        self.log('dbca配置成功，请在节点{}上使用oracle用户执行dbca建库脚本：/u01/app/oracle/product/19.0.0/dbhome_1/bin/dbca -silent -createDatabase -ignorePrereqFailure '
                 '-responseFile /tmp/dbca.rsp'
                 ' 并根据提示执行后续脚本'.format(self.node_info['node_ip']))
                 
        self.log('DBCA建库成功后，创建数据库监听：netca -silent -responsefile /u01/app/oracle/product/19.0.0/dbhome_1/assistants/netca/netca.rsp')

        # 开始静默安装
        # self.log('开始进行dbca静默安装，请关注{}：/tmp/dbca.log'.format(node['ip']))
        # cmd = '/u01/app/oracle/product/19.0.0/dbhome_1/bin/dbca -silent -createDatabase -ignorePrereqFailure ' \
        #       '-responseFile /tmp/dbca.rsp > /tmp/dbca.log'
        # LinuxBase(oracle_params).exec_command_res(cmd)
        # self.log('dbca静默安装完成..')

    def do_onenode_install(self,module):
        if module == 'linux':
            self.log('linux基础配置已启动..')
            self.clear_log()
            self.do_linux_config()
        elif module == 'oracle':
            self.log('oracle安装已启动..')
            self.oracle_install()
        elif module =='dbca':
            self.log('dbca建库已启动..')
            self.oracle_dbca()
        elif module == 'clear':
            self.log('开始清理Oracle安装..')
            self.clear_rac()
        else:
            print('输入参数不合法！')

if __name__ == '__main__':
    node_info = {
        'node_ip': '192.168.48.51',
        'hostname': 'cispdg',
        'dbname': 'cispcdb',
        'pdbname': 'cisp',
        'password': 'oracle',
    }

    oracleracinstall = OracleOneNodeInstall(node_info)
    # oracleracinstall.clear_rac()
    oracleracinstall.do_rac_install('linux')
