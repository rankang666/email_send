#!/usr/bin/env python
# encoding: utf-8
'''
@Time: 2022/7/21 19:10
@Project: mmb 
@File: SendEmail.py
@Author: rk
@Software: pycharm
@Desc: 邮箱发送功能
'''
import smtplib

from email_utils.EmailContent import EmailContent


class SendEmail:

    def __init__(self,smtpHost,port,senduser,password,buglevel=False):
        '''
        登录信息
        :param smtpHost: SMTP的服务器信息
        :param port: port = 25 【不使用TLS】smtplib.SMTP【TLS禁用时使用】
                    port = 465 【使用TLS】smtplib.SMTP_SSL【开启TLS时使用】
        :param user: 用户地址
        :param password: 用户密码
        :param buglevel: 设置debug模块
        '''
        if port == 25:
            self.smtpServer = smtplib.SMTP(smtpHost,port)
        elif port == 465:
            self.smtpServer = smtplib.SMTP_SSL(smtpHost,port)
        else:
            print('暂不支持此端口,请调整')
        # 设置debug模块
        self.smtpServer.set_debuglevel(buglevel)
        # 登录
        self.senderAdr = senduser
        self.smtpServer.login(senduser, password)

        print('发送用户({})登录成功'.format(senduser))

    def setSubject(self,toReceivers,ccReceivers,header,emailSubject):
        self.toAddrs = toReceivers + ccReceivers
        self.emailContent = EmailContent(header, emailSubject, toReceivers, ccReceivers)

    def setContent(self, info, bodyType='string', img_path=None, attachment_file=None):
        self.emailContent.addBody(info, bodyType, img_path)
        if attachment_file:
            self.emailContent.addAttachment(attachment_file)

    def send(self):
        if  not self.emailContent:
            print('请先配置接收信息(setSubject&setContent)')
            return
        message = self.emailContent.msg
        # 发送
        self.smtpServer.sendmail(self.senderAdr,self.toAddrs,message.as_string())
        print('已发送成功')
        # 终止SMTP会话
        self.smtpServer.quit()