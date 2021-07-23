import threading
import time
from utils import *
import main_test
import is_full

def cs_send_log():
    while True:
        if time.localtime(time.time()).tm_min == 0:
            bm = BaseInformation(basePath)
            sc = SelfCheck()
            logger = MyLogger(bm.basePath + r'/utils/log_c.txt', "client_logger")
            db = DataBase()
            cpuTemp = sc.getCPUtemperature()
            cpuUsed = sc.getCPUuse()
            ramInfo = sc.getRAMinfo()
            diskInfo = sc.getDiskSpace()
            fp = sc.checkFpMD5(bm.get_fp_MD5())
            msg = 'client_ID=' + bm.get_client_ID() + '\n' + 'client_username=' + bm.get_client_username() + '\n' + 'client_location=' + bm.get_client_location() + '\n' + cpuTemp + '\n' + cpuUsed + '\n' + ramInfo + '\n' + diskInfo + '\n' + 'changedFilePath=' + ','.join(
                fp)
            msg = msg.replace(' ', '')
            logger.log_info('\n' + msg)

            data = tuple([k.split('=')[1] for k in msg.split('\n')])

            cmd = "INSERT INTO INFO(TIME,CLIENT_ID,CLIENT_USERNAME,CLIENT_LOCATION, CPUTEMPERATURE, CPUUSE,RAMTOTAL ,  RAMUSED ,  RAMFREE ,  DISKTOTALSPACE ,  DISKUSEDSPACE,  DISKUSEDPERCENTAGE ,  CHANGEDFILEPATH )VALUES(now(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % data
            db.execute(cmd)

        if is_full.jianman():
            db = DataBase()
            bm = BaseInformation(basePath)
            status = "full"
            cmd = "INSERT INTO STATUS(TIME,CLIENT_ID,status)VALUES(now(),'%s','%s')" % (bm.get_client_ID(), status)
            db.execute(cmd)
        else:
            db = DataBase()
            bm = BaseInformation(basePath)
            status = "not full"
            cmd = "INSERT INTO STATUS(TIME,CLIENT_ID,status)VALUES(now(),'%s','%s')" % (bm.get_client_ID(), status)
            db.execute(cmd)
        time.sleep(5)


def main():
    t1 = threading.Thread(target=cs_send_log)
    t1.start()

    main_test.main()


if __name__ == '__main__':
    main()
