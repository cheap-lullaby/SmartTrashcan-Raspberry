import hashlib
import logging
import pymysql
import os
import random
import string
from configparser import ConfigParser

basePath = r'/home/pi/Desktop/SmartTrashcan'


class MyConfigParser(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class MyLogger(object):
    def __init__(self, logPath, loggerName):
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.INFO)
        self.fh = logging.FileHandler(logPath)
        self.fh.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s  - %(levelname)s: %(message)s")
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def log_info(self, msg):
        self.logger.info(msg)

    def log_warning(self, msg):
        self.logger.warning(msg)


class BaseInformation(object):
    def __init__(self, basePath):
        self.cp = MyConfigParser()
        self.basePath = basePath
        self.baseInfoPath = self.basePath + r'/utils/baseInfo.ini'

        if not os.path.exists('utils'):
            os.mkdir('utils')

    def get_client_ID(self):
        try:
            self.cp.read(self.baseInfoPath)
            client_ID = self.cp.get('baseInfo', 'client_ID')
        except Exception:
            client_ID = self.set_client_ID()
        return client_ID

    def get_client_username(self):
        try:
            self.cp.read(self.baseInfoPath)
            client_username = self.cp.get('baseInfo', 'client_username')
        except Exception:
            client_username = self.set_client_username()
        return client_username

    def get_client_location(self):
        try:
            self.cp.read(self.baseInfoPath)
            client_location = self.cp.get('baseInfo', 'client_location')
        except Exception:
            client_location = self.set_client_location()
        return client_location

    def get_fp_MD5(self):
        fp_MD5 = {}
        try:
            self.cp.read(self.baseInfoPath)
            fp_MD5 = dict(self.cp.items('fp_MD5'))
        except Exception:
            fp_MD5 = self.set_fp_MD5(fp_MD5)
        return fp_MD5

    def set_client_ID(self, client_ID=None):
        if client_ID is None:
            client_ID = "".join([random.choice(string.ascii_letters + string.digits) for i in range(16)])
        self.cp.read(self.baseInfoPath)
        if 'baseInfo' not in self.cp.sections():
            self.cp.add_section('baseInfo')
        self.cp.set('baseInfo', 'client_ID', client_ID)
        with open(self.baseInfoPath, "w") as f:
            self.cp.write(f)
        return client_ID

    def set_client_username(self, client_username=None):
        if client_username is None:
            client_username = 'garbage' + "".join([random.choice(string.digits) for i in range(random.randint(1, 3))])
        self.cp.read(self.baseInfoPath)
        if 'baseInfo' not in self.cp.sections():
            self.cp.add_section('baseInfo')

        self.cp.set('baseInfo', 'client_username', client_username)
        with open(self.baseInfoPath, "w") as f:
            self.cp.write(f)
        return client_username

    def set_client_location(self, client_location=None):
        if client_location is None:
            client_location = "unKnow"
        self.cp.read(self.baseInfoPath)
        if 'baseInfo' not in self.cp.sections():
            self.cp.add_section('baseInfo')
        self.cp.set('baseInfo', 'client_location', client_location)
        with open(self.baseInfoPath, "w") as f:
            self.cp.write(f)
        return client_location

    def set_fp_MD5(self, fp_MD5):
        if len(fp_MD5) == 0:
            for root, dirs, files in os.walk(self.basePath):
                for f in files:
                    fp_MD5[os.path.join(root, f)] = MD5(os.path.join(root, f))
        self.cp.read(self.baseInfoPath)
        if 'fp_MD5' not in self.cp.sections():
            self.cp.add_section('fp_MD5')
        for fp in fp_MD5:
            self.cp.set('fp_MD5', fp, fp_MD5[fp])

        with open(self.baseInfoPath, "w") as f:
            self.cp.write(f)
        return fp_MD5


class SelfCheck(object):
    def __init__(self):
        pass

    def getCPUtemperature(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return ('CPU Temperature= ' + res.replace("temp=", "").replace("'C\n", "") )

    def getCPUuse(self):
        return ('CPU Use =' + str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))           

    def getRAMinfo(self):
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i == 2:
                RAM_stats = line.split()[1:4]
                RAM_total = round(int(RAM_stats[0]) / 1000, 1)
                RAM_used = round(int(RAM_stats[1]) / 1000, 1)
                RAM_free = round(int(RAM_stats[2]) / 1000, 1)
                return 'RAM Total= ' + str(RAM_total) + ' MB\n' + \
                       'RAM Used= ' + str(RAM_used) + ' MB\n' + \
                       'RAM Free= ' + str(RAM_free) + ' MB'

    def getDiskSpace(self):
        p = os.popen("df -h /")
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i == 2:
                DISK_stats = line.split()[1:5]
                DISK_total = DISK_stats[0]
                DISK_used = DISK_stats[1]
                DISK_perc = DISK_stats[3]

                return 'DISK Total Space= ' + str(DISK_total) + 'B\n' + \
                       'DISK Used Space= ' + str(DISK_used) + 'B\n' + \
                       'DISK Used Percentage= ' + str(DISK_perc)

    def checkFpMD5(self, fp_MD5):
        wp = []
        for fp in fp_MD5:
            if fp_MD5[fp] != MD5(fp):
                wp.append(fp)
        return wp


class DataBase(object):
    def __init__(self):
        self._conn = pymysql.connect(
            host='47.240.131.162',
            user='root',
            password='123456',
            database='lajitongweb',
            charset='utf8'
        )

        self._cursor = self._conn.cursor()
        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS INFO    (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,TIME TIMESTAMP NOT NULL,CLIENT_ID CHAR(16) NOT NULL,CLIENT_USERNAME CHAR(10) NOT NULL,CLIENT_LOCATION CHAR(20) NOT NULL, CPUTEMPERATURE  CHAR(6) NOT NULL, CPUUSE CHAR(6) NOT NULL,RAMTOTAL  CHAR(10)  NOT NULL,  RAMUSED  CHAR(10) NOT NULL,  RAMFREE  CHAR(10)  NOT NULL,  DISKTOTALSPACE  CHAR(10) NOT NULL,  DISKUSEDSPACE CHAR(10) NOT NULL,  DISKUSEDPERCENTAGE  CHAR(6)    NOT NULL,  CHANGEDFILEPATH  LONGTEXT NOT NULL);')
        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS STATUS  (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,TIME TIMESTAMP NOT NULL,CLIENT_ID CHAR(16) NOT NULL,STATUS CHAR(10) NOT NULL);')
        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS CLASSIFY(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,TIME TIMESTAMP NOT NULL,CLIENT_ID CHAR(16) NOT NULL,RESULT CHAR(6) NOT NULL, RELIABLITY CHAR(6) NOT NULL);')

    def execute(self, cmd):
        return self._cursor.execute(cmd)

    def __del__(self):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()


def MD5(fp):
    with open(fp, 'rb') as f:
        hl = hashlib.md5((f.read()))
    return hl.hexdigest()
if __name__ == '__main__':
    SelfCheck().getDiskSpace()