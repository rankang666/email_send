#!/usr/bin/env python
# encoding: utf-8
'''
@Time: 2022/4/29 15:33
@Project: pythonProject 
@File: EmailContent.py
@Author: rk
@Software: pycharm
@Desc: 邮箱正文 添加内容/附件
'''
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os


class EmailContent:

    def __init__(self, header, emailSubject, toReceivers, ccReceivers):
        # 邮件对象
        self.msg = MIMEMultipart()
        # 添加发件人头
        self.msg['From'] = Header(header, 'utf-8')
        # 添加邮件主题
        self.msg['Subject'] = Header(emailSubject, "utf-8")
        # 添加收件人
        self.msg['To'] = ";".join(toReceivers)
        # 添加抄送人
        self.msg["Cc"] = ";".join(ccReceivers)

    def addBody(self, info, bodyType='string', img_path=None):
        """
        添加不同的邮件正文的实例
        1. body为字符串：(如)"这是一个邮件正文内容"
        2. body为html格式的字符串：(如)"<div><p>第一段</p><p>&nbsp;第二段</p></div>"
        3. body正文中包含有图片：
        """
        print('邮件类型:',bodyType)

        mimeText = None
        if bodyType == "string":
            mimeText = MIMEText(info, "plain", "utf-8")
        elif bodyType == "html":
            mimeText = MIMEText(info, "html", "utf-8")
        elif "image" in bodyType:
            mimeText = MIMEText(info, "html", "utf-8")
            if not img_path:
                print('请输入图片路径img_path')
                return
            # 读取图片，并设置图片id用于邮件正文引用
            filePath, imgName = os.path.split(img_path)
            print('imgpath: ',img_path)
            with open(img_path, "rb") as fp:
                mimeImage = MIMEImage(fp.read())
            mimeImage.add_header("Content-ID", imgName)
            self.msg.attach(mimeImage)
        else:
            print('指定类型错误,目前只支持string/html/image')
            return
        self.msg.attach(mimeText)

    def addAttachment(self,attachment_path):
        """
        添加附件
        :return:
        """
        _, fileName = os.path.split(attachment_path)
        print("追加附件: ", fileName)
        enclosure = MIMEText(open(attachment_path, 'rb').read(), 'base64', 'utf-8')
        enclosure['Content-Type'] = 'application/octet-stream'
        enclosure.add_header("Content-Disposition", "attachment", filename=("gbk", "", fileName))
        self.msg.attach(enclosure)








