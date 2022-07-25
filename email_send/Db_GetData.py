#!/usr/bin/env python
# encoding: utf-8
'''
@Time: 2022/7/20 20:30
@Project: mmb 
@File: Db_GetData.py
@Author: rk
@Software: pycharm
@Desc:
'''
import datetime
import os

import pandas as pd

from Db_Mysql import Db_Mysql
from Db_Odps import Db_Odps
from Db_SqlServer import Db_SqlServer


class Db_GetData():
    # 保存数据
    def saveData(self, name, df_maps, header=True):
        path = os.path.abspath(name)
        writer = pd.ExcelWriter(name)
        for sheet, df in df_maps.items():
            if df.columns.isnull().all():
                header = False
            df.to_excel(writer, sheet_name=sheet, index=False, header=header)
        writer.save()

        print('数据保存到:{}'.format(path))
        return path

    # 删除历史数据
    def deleteHistoryFile(self, save_file, day=3):
        path, file_name = os.path.split(os.path.abspath(save_file))
        # 当前生成文件的最新时间
        file_dt = datetime.datetime.strptime(file_name.split('_')[1].split('.')[0], '%Y%m%d')
        # 当前生成文件名称中的关键词
        file_key = file_name.split('_')[0]

        for file_path, _, files in os.walk(path):
            for file in files:
                if file_key in file and len(file.split('_')) > 1:
                    # 历史文件的文件生成时间
                    dt = datetime.datetime.strptime(file.split('_')[1].split('.')[0], '%Y%m%d')
                    if (file_dt - dt).days > day:
                        print('{}文件大于{}天删除'.format(file, day))
                        os.remove(os.path.join(file_path, file))

    # 运行
    def run(self, save_path, tables, type='odps'):
        df_maps = dict()
        if type == 'odps':
            db_odps = Db_Odps()
            df_maps = db_odps.runOdps(tables)
        elif type == 'sqlserver':
            db_sqlserver = Db_SqlServer()
            df_maps = db_sqlserver.runSqlserver(tables)
        elif type == 'mysql':
            db_mysql = Db_Mysql()
            df_maps = db_mysql.runMysql(tables)

        # 批量保存数据
        save_path = self.saveData(save_path, df_maps)
        # 清除前3天历史数据
        self.deleteHistoryFile(save_path)