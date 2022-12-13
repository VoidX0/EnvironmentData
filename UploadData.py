#! /usr/bin/python3
import Environment
import DeviceStatus
import NetworkStatus
import json
import time
import pymysql


class UploadData(object):
    """
        上传数据
    """
    def __init__(self, interval):
        """
            初始化上传
        """
        if not self._dbInit():
            print('数据库连接失败，请检查连接')
            return
        self.Sensor = Environment.Environment(17)
        self.Device = DeviceStatus.DeviceStatus()
        self.Network = NetworkStatus.NetworkStatus()
        while True:
            print('>>>  Start  <<<')
            self._upload()
            time.sleep(interval)

    def _dbInit(self):
        """
        数据库连接初始化
        """
        # 新建连接
        with open('config.json') as _configJson:
            _config = json.load(_configJson)
        _dbConfig = _config['connections'][int(_config['connectionSelect'])]
        try:
            self._connection = pymysql.connect(host=_dbConfig['host'],
                                               database=_dbConfig['database'],
                                               user=_dbConfig['user'],
                                               password=_dbConfig['password'])
            return True
        # 连接字典错误
        except Exception as ex:
            print('Exception:\n' + str(ex))
            return False

    def _upload(self):
        """
            数据上传数据库
        """
        self.Sensor.refresh()
        self.Device.refresh()
        self.Network.refresh()
        cursor = self._connection.cursor()
        try:
            if self.Sensor.Temperature != 0 and self.Sensor.Humidity != 0:
                cursor.execute(
                    "INSERT INTO Environment(Temperature, Humidity, RecordTime) VALUES({0}, {1}, '{2}')"
                    .format(self.Sensor.Temperature, self.Sensor.Humidity,
                            self.Sensor.Time))
            cursor.execute(
                "INSERT INTO DeviceStatus(CPUTemperature, CPUOccupancyRate, RAMOccupancyRate, SDCardOccupancyRate, HDDOccupancyRate, Upload, Download, RecordTime) VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6}, '{7}')"
                .format(self.Device.CPUTemperature,
                        self.Device.CPUOccupancyRate,
                        self.Device.RAMOccupancyRate,
                        self.Device.SDCardOccupancyRate,
                        self.Device.HDDOccupancyRate,
                        self.Network.Upload,
                        self.Network.Download,
                        self.Device.Time))
            self._connection.commit()
        except Exception as ex:
            print("Upload Error:\n" + str(ex))
            self._connection.rollback()
        cursor.close()


if __name__ == "__main__":
    with open('config.json') as configJson:
        config = json.load(configJson)
    UploadData(int(config['TimerInterval']))
