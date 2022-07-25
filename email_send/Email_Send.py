#!/usr/bin/env python
# encoding: utf-8
'''
@Time: 2022/5/5 9:35
@Project: pythonProject 
@File: email_main.py
@Author: rk
@Software: pycharm
@Desc: 邮箱发送实现
'''
import datetime

from email_send.Db_GetData import Db_GetData
from email_utils.SendEmail import SendEmail

def send_email():
    # SMTP的服务器信息|用户信息 linux 465
    smtpHost = "smtp.exmail.qq.com"
    port = 25
    senduser = "******"
    senderPwd = "******"
    # 登录
    sender = SendEmail(smtpHost, port, senduser, senderPwd, buglevel=False)
    print('邮箱登录成功')
    return sender

def formatParam(save_path,bizdate=None):
    # 设置时间
    if not bizdate:
        now_time = datetime.datetime.now()
        bizdate = (now_time + datetime.timedelta(days=-1)).strftime('%Y%m%d')

    # 给文件名追加时间 返利网H5页面事项统计表.xlsx -> 返利网H5页面事项统计表_20220505.xlsx
    if bizdate not in save_path:
        save_path = '{}_{}.{}'.format(save_path.split('.')[0], bizdate, save_path.split('.')[1])
    return bizdate, save_path

if __name__== '__main__':
    # 将统计数据写入文件
    df = Db_GetData()
    # 文件保存路径
    save_path = '统计表.xlsx'

    # 格式化参数 bizdate， sava_path bizdate默认前一天
    # bizdate不指定，默认会在生成文件名后追加 返利网H5页面事项统计表.xlsx -> 返利网H5页面事项统计表_20220505.xlsx
    bizdate, save_path = formatParam(save_path)
    # 获取时间bizdate-1
    bizdate_1 = (datetime.datetime.strptime(bizdate, "%Y%m%d") + datetime.timedelta(days=-1)).strftime('%Y%m%d')
    # sheet页名称 表名称 分区日期
    tables = [('sheet1', 'table1', bizdate_1)
        , ('sheet2', 'table2', bizdate)]

    # 将结果保存到指定路径
    df.run(save_path, tables, type='odps')

    # sheet table time
    # tables = [('测试', 'dbo.table', bizdate_1,'主键,名称,,,,,,,,,,,,')]
    # df.run(save_path, tables, type='sqlserver')

    # 将文件作为附件发送到邮箱
    sender = send_email()
    # 配置接收者/标题
    toReceivers = ["********@163.com"]
    ccReceivers = []
    header = '每日数据统计'
    subject = "数据主题"
    sender.setSubject(toReceivers, ccReceivers, header, subject)

    # 发送内容及附件
    info = '{}的统计数据'.format(bizdate)
    sender.setContent(info,attachment_file=save_path)

    # 发送
    sender.send()












