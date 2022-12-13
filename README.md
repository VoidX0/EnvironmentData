# 树莓派环境监测系统
- 树莓派使用Adafruit库，传感器为DHT11
- 使用数据库为MySql8
- 定时采集数据，并上传数据库
###快捷启动
```
.zshrc添加
alias env_data="cd ~/source/Python/EnvironmentData/ && sudo python3 UploadData.py"
```