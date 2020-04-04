# coding=gbk
import csv
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("���ڷ��ͼ�������")

url = r'https://free-api.heweather.net/s6/weather/forecast?location=����&key=3a5c6118fc7143a5a1ea56f01f950bdc'
# ��ȡ����ʱ��	2020-3-5
today_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

def get_weather_data():
    res = requests.get(url).json()
    # res.encoding = 'utf-8'
    result = res['HeWeather6'][0]['daily_forecast']
    location = res['HeWeather6'][0]['basic']
    city = location['parent_city'] + location['location']
    names = ['����', 'ʱ��', '����״��', '�����', '�����', '�ճ�', '����']
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
    # �������������
    HOST = 'smtp.qq.com'
    # �����ʼ�����
    SUBJECT = '%s�շ�����Ԥ����Ϣ�������'%today_time
    # ���÷���������
    FROM = 'xxx@xxx.com'
    # �����ռ�������
    TO = 'xxx@xxx.com'		# ����ͬʱ���͵��������,���Ÿ���
    message = MIMEMultipart('related')
    # --------------------------------------�����ı�-----------------
	# �����ʼ����ĵ��Է���������
    message_html = MIMEText("%s�շ�����Ԥ�����ˣ������" % today_time, 'plain', 'utf-8')
    message.attach(message_html)

    # -------------------------------------����ļ�---------------------
    # today_weather.csv����ļ�
    message_xlsx = MIMEText(open('today_weather.csv', 'rb').read(), 'base64', 'utf-8')
    # �����ļ��ڸ������е�����
    message_xlsx['Content-Disposition'] = 'attachment;filename="today_weather.csv"'
    message.attach(message_xlsx)

    # �����ʼ�������
    message['From'] = "����С����"
    # �����ʼ��ռ���
    message['To'] = "xxx@xxx.com"
    # �����ʼ�����
    message['Subject'] = SUBJECT

    # ��ȡ���ʼ�����Э���֤��
    email_client = smtplib.SMTP_SSL(host='smtp.qq.com')
    # ���÷���������������Ͷ˿ڣ��˿�Ϊ465
    email_client.connect(HOST, '465')
    # ---------------------------������Ȩ��------------------------------
    result = email_client.login(FROM, 'fsqjuzbpmmmxbdaj')
    print('��¼���', result)
    email_client.sendmail(from_addr=FROM, to_addrs=TO.split(','), msg=message.as_string())
    # �ر��ʼ����Ϳͻ���
    email_client.close()

get_weather_data()