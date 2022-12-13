#! /usr/bin/python3
import psutil
import time
import datetime

class NetworkStatus(object):
    """
        网络状态
    """
    def __init__(self):
        self.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.Upload = 0
        self.Download = 0

    def refresh(self):
        """
            刷新网络状态
        """
        sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        time.sleep(1)
        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        self.Upload = round((sent_now - sent_before)/1024, 2)  # 算出1秒后的差值
        self.Download = round((recv_now - recv_before)/1024, 2)
        self.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('上传：{0}KB/s  下载：{1}KB/s  Time:{2}'.format(
                self.Upload, self.Download, self.Time))

if __name__ == "__main__":
    NetworkStatus().refresh()
