# coding=gbk
import csv
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("正在发送嘉兴天气")

url = r'https://free-api.heweather.net/s6/weather/forecast?location=嘉兴&key=3a5c6118fc7143a5a1ea56f01f950bdc'
# 获取当日时间	2020-3-5
today_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

def get_weather_data():
    res = requests.get(url).json()
    # res.encoding = 'utf-8'
    result = res['HeWeather6'][0]['daily_forecast']
    location = res['HeWeather6'][0]['basic']
    city = location['parent_city'] + location['location']
    names = ['城市', '时间', '天气状况', '最高温', '最低温', '日出', '日落']
    with open('today_weather.csv', 'w', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(names)
        for data in result:
            date = data['date']
            cond = data['cond_txt_d']
            max = data['tmp_max']
            min = data['tmp_min']
            sr = data['sr']
            ss = data['ss']
            writer.writerows([(city, date, cond, max, min, sr, ss)])
    send_email()

def send_email():
    # 设置邮箱的域名
    HOST = 'smtp.qq.com'
    # 设置邮件标题
    SUBJECT = '%s日份天气预报信息，请查收'%today_time
    # 设置发件人邮箱
    FROM = 'xxx@xxx.com'
    # 设置收件人邮箱
    TO = 'xxx@xxx.com'		# 可以同时发送到多个邮箱,逗号隔开
    message = MIMEMultipart('related')
    # --------------------------------------发送文本-----------------
	# 发送邮件正文到对方的邮箱中
    message_html = MIMEText("%s日份天气预报到了，请查收" % today_time, 'plain', 'utf-8')
    message.attach(message_html)

    # -------------------------------------添加文件---------------------
    # today_weather.csv这个文件
    message_xlsx = MIMEText(open('today_weather.csv', 'rb').read(), 'base64', 'utf-8')
    # 设置文件在附件当中的名字
    message_xlsx['Content-Disposition'] = 'attachment;filename="today_weather.csv"'
    message.attach(message_xlsx)

    # 设置邮件发件人
    message['From'] = "天气小助手"
    # 设置邮件收件人
    message['To'] = "xxx@xxx.com"
    # 设置邮件标题
    message['Subject'] = SUBJECT

    # 获取简单邮件传输协议的证书
    email_client = smtplib.SMTP_SSL(host='smtp.qq.com')
    # 设置发件人邮箱的域名和端口，端口为465
    email_client.connect(HOST, '465')
    # ---------------------------邮箱授权码------------------------------
    result = email_client.login(FROM, 'fsqjuzbpmmmxbdaj')
    print('登录结果', result)
    email_client.sendmail(from_addr=FROM, to_addrs=TO.split(','), msg=message.as_string())
    # 关闭邮件发送客户端
    email_client.close()

get_weather_data()