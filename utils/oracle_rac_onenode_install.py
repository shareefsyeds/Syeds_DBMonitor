# encoding： utf-8

from utils.linux_base import LinuxBase
from utils.tools import now_local
from utils.tools import mysql_exec,mysql_query,now,get_memtotal
import os

class OracleRacOneNodeInstall():
    def __init__(self, node_info):
        self.node_info = node_info
        self.linux_group_list = [
            [5000, 'asmadmin'],
            [5001, 'asmdba'],
            [5002, 'asmoper'],
            [5003, 'dba'],
            [5004, 'oper'],
            [5005, 'backupdba'],
            [5006, 'dgdba'],
            [5007, 'kmdba'],
            [5008, 'racdba'],
            [5009, 'oinstall']
        ]
        self.linux_user_list = {
            'grid': 5010,
            'oracle': 5011
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
        log_type = 'Oracle RAC The installation'
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
            ['userdel -rf grid',
            'userdel -rf oracle'],
        )
        # Remove the ASM information
        cmd_list.extend(
            ['dd if=/dev/zero of={} bs=8192 count=2147'.format(self.node_info['ocr_disk']),
            'dd if=/dev/zero of={} bs=8192 count=2147'.format(self.node_info['data_disk'])]
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
        self.log('Oracle RAC cleanup completed！')


    def upload_software(self, linux_params):
        # File upload
        LinuxBase(linux_params).sftp_upload_file('{}grid_profile'.format(self.local_path), '/tmp/grid_profile')
        LinuxBase(linux_params).sftp_upload_file('{}oracle_profile'.format(self.local_path), '/tmp/oracle_profile')
        LinuxBase(linux_params).sftp_upload_file('{}compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm'.format(self.local_path),
                                                 '/tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm')
        LinuxBase(linux_params).sftp_upload_file('{}cvuqdisk-1.0.10-1.rpm'.format(self.local_path),
                                                 '/tmp/cvuqdisk-1.0.10-1.rpm')
        LinuxBase(linux_params).sftp_upload_file('{}97-oracle-database-sysctl.conf'.format(self.local_path),
                                                 '/tmp/97-oracle-database-sysctl.conf')
        LinuxBase(linux_params).sftp_upload_file('{}oracle-database-preinstall-19c.conf'.format(self.local_path),
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
            'userdel -rf grid',
            'userdel -rf oracle',
            'useradd -u {} -g oinstall -G asmadmin,asmdba,racdba,asmoper grid'.format(self.linux_user_list['grid']),
            'useradd -u 5011 -g oinstall -G dba,asmdba,backupdba,dgdba,kmdba,racdba,oper oracle'.format(
                self.linux_user_list['oracle']),
            "echo 'grid:oracle'|chpasswd",
            "echo 'oracle:oracle'|chpasswd"
        ])

        # Create a directory, authorization
        cmd_list.extend([
            'rm -rf /u01',
            'mkdir -p /u01/app/19.0.0/grid',
            'mkdir -p /u01/app/grid',
            'mkdir -p /u01/app/oracle/product/19.0.0/dbhome_1/',
            'mkdir -p /u01/app/oraInventory',
            'chown -R grid:oinstall /u01',
            'chown -R oracle:oinstall /u01/app/oracle',
            'chmod -R 775 /u01/'
        ])

        # yum Install required packages
        cmd_list.extend([
            'yum -y install {}'.format(self.linux_packages),
            'rpm -ivh /tmp/compat-libstdc++-33-3.2.3-72.el7.x86_64.rpm',
            'rpm -ivh /tmp/cvuqdisk-1.0.10-1.rpm'
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

        # Close the avahi - daemon service
        cmd_list.extend([
            'systemctl stop avahi-daemon.socket',
            'systemctl stop avahi-daemon.service',
            'systemctl disable avahi-daemon.socket',
            'systemctl disable avahi-daemon.service'
            ]
        )

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
            'mv /tmp/grid_profile /home/grid/.bash_profile',
            'chown grid:oinstall /home/grid/.bash_profile',
            "sed -i 's/NODE_ASM_SID/{}/g' /home/grid/.bash_profile".format('+ASM'),
            'mv /tmp/oracle_profile /home/oracle/.bash_profile',
            'chown oracle:oinstall /home/oracle/.bash_profile',
            "sed -i 's/NODE_ORACLE_SID/{}/g' /home/oracle/.bash_profile".format(
                self.node_info['dbname'])
        ])

        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('{} {}：linux The operating system configuration is complete'.format(self.node_info['node_ip'], self.node_info['hostname']))

        self.log('linux Basic configuration is complete！')

    def grid_execute_scripts(self):
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'root',
            'password': self.node_info['node_password']
        }
        linux_conn, _ = LinuxBase(linux_params).connection()

        cmd = '/u01/app/oraInventory/orainstRoot.sh'
        LinuxBase(linux_params).exec_command_res(cmd,linux_conn)

        cmd = '/u01/app/19.0.0/grid/root.sh'
        LinuxBase(linux_params).exec_command_res(cmd,linux_conn)


    def grid_install(self):
        self.log('To begin the grid clustering software installation..')
        # Only in the first node operation
        linux_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'grid',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(linux_params).connection()
        # Upload the grid installation package
        self.log('{} {}：Start Posting the grid installation package..'.format(self.node_info['node_ip'], self.node_info['hostname']))
        LinuxBase(linux_params).sftp_upload_file('{}LINUX.X64_193000_grid_home.zip'.format(self.local_path), '/tmp/LINUX.X64_193000_grid_home.zip')
        self.log('grid The installation package to upload to complete！')

        self.log('{} {}：Began to unpack the grid installation package！'.format(self.node_info['node_ip'], self.node_info['hostname']))
        cmd = 'unzip -q -o /tmp/LINUX.X64_193000_grid_home.zip -d /u01/app/19.0.0/grid/'
        LinuxBase(linux_params).exec_command_res(cmd,linux_conn)
        self.log('grid The installation package decompression！')
        cmd = 'rm -f /tmp/LINUX.X64_193000_grid_home.zip'
        LinuxBase(linux_params).exec_command_res(cmd,linux_conn)
        self.log('grid The installation package clean finish！')

        self.log('The response file to start generating grid installation..')
        LinuxBase(linux_params).sftp_upload_file('{}gridsetup_onenode.rsp'.format(self.local_path), '/tmp/gridsetup.rsp')

        # Modify the response file
        cmd_list = [
            "sed -i 's#NODE_OCR_DISK#{}#g' /tmp/gridsetup.rsp".format(self.node_info['ocr_disk']),
            "sed -i 's#NODE_OCR_PATH#{}#g' /tmp/gridsetup.rsp".format(self.node_info['disk_path'])
        ]
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('The grid installation response cannot be completed！')

        # Silent installation
        self.log('grid The cluster configuration is successful, please perform on the node {} silent installation：/u01/app/19.0.0/grid/gridSetup.sh -silent -ignorePrereqFailure -responseFile /tmp/gridsetup.rsp'
                 ' And according to the prompt implementation root. Sh scripts'.format(self.node_info['node_ip']))

        # Perform silent installation
        # the self. The log (' silent installation start executing cluster software..Please pay attention to the grid installation log {} : / TMP/gridsetup. Log '. The format (node [' IP ']))
        # CMD = '/ u01 / app / 19.0.0 / grid/gridSetup. Sh - silent - ignorePrereqFailure - responseFile/TMP/gridSetup RSP > / TMP/gridSetup log'
        # LinuxBase (linux_params). Exec_command_res (CMD)
        # the self. The log (' grid cluster a silent installation is complete!')
        # the self. The log (' according to the/TMP/gridsetup. Please log in the tip executing scripts!')
        # silent installation script execution
        # self. Grid_execute_scripts ()

        # Perform configuration tool script
        cmd = '/u01/app/19.0.0/grid/gridSetup.sh -executeConfigTools -responseFile /tmp/gridsetup.rsp -silent'
        # LinuxBase(linux_params).exec_command_res(cmd)

        # After installation
        # $ORACLE_HOME/runcluvfy.sh  stage -post  crsinst -n "cispdb1,cispdb2"  -verbose

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
        self.log('oracle The installation package to upload to complete！')
        self.log('Started to unzip the oracle installation package..')
        cmd = 'unzip -q -o /tmp/LINUX.X64_193000_db_home.zip -d /u01/app/oracle/product/19.0.0/dbhome_1/'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('oracle The installation package decompression！')
        cmd = 'rm -f /tmp/LINUX.X64_193000_db_home.zip'
        LinuxBase(linux_params).exec_command_res(cmd)
        self.log('oracle The installation package clean finish！')

        self.log('Begin to generate oracle install response file..')
        LinuxBase(linux_params).sftp_upload_file('{}db_install_onenode.rsp'.format(self.local_path), '/tmp/db_install.rsp')

        # Modify the response file
        cmd_list = [
            "sed -i 's/NODE_HOSTNAME/{}/g' /tmp/db_install.rsp".format(self.node_info['hostname']),
        ]
        res = [LinuxBase(linux_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('The oracle install response cannot be completed！')

        self.log('Before installing the oracle software configuration is successful, please use oracle users perform on the node {} silent installation script：'
                 '/u01/app/oracle/product/19.0.0/dbhome_1/runInstaller -silent -ignorePrereqFailure -responsefile /tmp/db_install.rsp '
                 ' And according to the prompt follow-up script execution'.format(self.node_info['node_ip']))

        # silent installation
        # the self. The log (' start Oracle software silent installation, pay attention to {} : / TMP/oraclesetup log '. The format (node (IP)))
        # CMD = '/ u01 / app/oracle/product / 19.0.0 / dbhome_1 / runInstaller - silent - ignorePrereqFailure - responsefile/TMP/db_install RSP > / TMP/oraclesetup log'
        # LinuxBase (linux_params). Exec_command_res (CMD)
        # self. The log (' silent Oracle software installation is complete!')
        # the self. The log (' according to the/TMP/oraclesetup. Please log in the tip executing scripts!')

        # Perform root script
        # self.oracle_execute_scripts()

    def oracle_dbca(self):
        self.log('To begin building library dbca..')
        grid_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'grid',
            'password': 'oracle'
        }
        self.log('Began to create the ASM disk group：DATA..')
        # Create the ASM disk group
        cmd = "/u01/app/19.0.0/grid/bin/asmca -silent -createDiskGroup -diskGroupName DATA -disk '{}' " \
              "-redundancy EXTERNAL -au_size 4 -compatible.asm '19.0.0.0.0' " \
              "-compatible.rdbms '19.0.0.0.0' -compatible.advm '19.0.0.0.0'".format(self.node_info['data_disk'])

        LinuxBase(grid_params).exec_command_res(cmd)
        self.log('ASM Disk group has been created！')

        oracle_params = {
            'hostname': self.node_info['node_ip'],
            'port': 22,
            'username': 'oracle',
            'password': 'oracle'
        }
        linux_conn, _ = LinuxBase(oracle_params).connection()

        self.log('To start generating dbca building response file..')
        LinuxBase(oracle_params).sftp_upload_file('{}dbca_onenode.rsp'.format(self.local_path), '/tmp/dbca.rsp')

        # Modify the response file
        cmd_list = [
            "sed -i 's/NODE_HOSTNAME/{}/g' /tmp/dbca.rsp".format(self.node_info['hostname']),
            "sed -i 's/NODE_DBNAME/{}/g' /tmp/dbca.rsp".format(self.node_info['dbname']),
            "sed -i 's/NODE_PDBNAME/{}/g' /tmp/dbca.rsp".format(self.node_info['pdbname'])
        ]
        res = [LinuxBase(oracle_params).exec_command_res(cmd, linux_conn) for cmd in cmd_list]
        self.log('dbca Building response cannot be completed！')

        self.log('Dbca configuration is successful, please in the node{}Use of oracle users perform dbca build script：/u01/app/oracle/product/19.0.0/dbhome_1/bin/dbca -silent -createDatabase -ignorePrereqFailure '
                 '-responseFile /tmp/dbca.rsp'
                 ' And according to the prompt follow-up script execution'.format(self.node_info['node_ip']))

        # start silent installation
        # the self. The log (' begin dbca silent installation, pay attention to {} : / TMP/dbca. Log '. The format (node [' IP ']))
        # CMD = '/ u01 / app/oracle/product / 19.0.0 / dbhome_1 / bin/dbca - silent - createDatabase - ignorePrereqFailure' \
        # '- responseFile/TMP/dbca. RSP > / TMP/dbca. Log'
        # LinuxBase (oracle_params). Exec_command_res (CMD)
        # the self. The log (' dbca silent installation is complete..')

    def do_rac_install(self,module):
        if module == 'linux':
            self.log('Linux based configuration is started..')
            self.clear_log()
            self.do_linux_config()
        elif module == 'rac':
            self.log('The grid installation is started..')
            self.grid_install()
        elif module == 'oracle':
            self.log('Oracle installation is started..')
            self.oracle_install()
        elif module =='dbca':
            self.log('dbca Building has started..')
            self.oracle_dbca()
        elif module == 'clear':
            self.log('Began to clean up Oracle rac..')
            self.clear_rac()
        else:
            print('The input parameter is illegal！')

if __name__ == '__main__':
    node_info = {
        'node_ip': '192.168.48.51',
        'hostname': 'cispdg',
        'dbname': 'cispcdb',
        'pdbname': 'cisp',
        'password': 'oracle',
        'ocr_disk': '/dev/mapper/asm-ocr',
        'disk_path': '/dev/mapper/asm*',
        'data_disk' : '/dev/mapper/asm-data'
    }

    oracleracinstall = OracleRacOneNodeInstall(node_info)
    # oracleracinstall.clear_rac()
    oracleracinstall.do_rac_install('linux')
