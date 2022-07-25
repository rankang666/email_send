#!/usr/bin/env python
# encoding: utf-8
'''
@Time: 2022/7/20 20:16
@Project: mmb 
@File: Db_Odps.py
@Author: rk
@Software: pycharm
@Desc:
'''
from odps import ODPS
from odps.models import Partition


class Db_Odps():
    # 获取ODPS连接
    def getOdpsConnect(self):
        # endpoint = 'http://service.cn-shenzhen.maxcompute.aliyun-inc.com/api'
        endpoint = "********"
        accessId = '********'
        accessKey = '********'
        project = '****'
        odps = ODPS(access_id=accessId, secret_access_key=accessKey, project=project, endpoint=endpoint)
        print('odps连接成功')
        return odps

    # 基于odps表解析配置信息
    def setOdpsTableInfos(self, odps, tables):
        # 存储表信息
        table_infos = dict()
        # 获取列注释，作为excel中字段名称
        for sheet, table, bizdate in tables:
            cols = odps.get_table(table).schema.columns
            col_comments = []
            for col in cols:
                if not isinstance(col, Partition):
                    col_comments.append(col.comment)
            partition = 'dt={}'.format(bizdate)
            # print('{}表---指定分区bizdate={}'.format(table,bizdate))
            table_info = {
                'table': table,
                'cols': col_comments,
                'partition': partition
            }
            table_infos['{}({})'.format(sheet, bizdate)] = table_info

        print('获取配置...', table_infos.keys())
        return table_infos

    # 获取Odps数据
    def getOdpsData(self, odps, table, partition, cols):
        df = odps.get_table(table).get_partition(partition).to_df().to_pandas()
        df.columns = cols
        print('获取{}表信息---分区为{}'.format(table, partition))
        # print(df.head(5))
        return df

    # odps运行
    def runOdps(self, tables):
        # 获取连接
        odps = self.getOdpsConnect()
        table_infos = self.setOdpsTableInfos(odps, tables)
        # 存储数据
        df_maps = dict()
        # 获取每个表数据并添加到df_maps
        for name, table_info in table_infos.items():
            # 获取数据
            df = self.getOdpsData(odps, table_info['table'], table_info['partition'], table_info['cols'])
            df_maps[name] = df
        return df_maps