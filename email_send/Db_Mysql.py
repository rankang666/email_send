#!/usr/bin/env python
# encoding: utf-8
'''
@Time: 2022/7/20 20:21
@Project: mmb 
@File: Db_mysql.py
@Author: rk
@Software: pycharm
@Desc:
'''
import pandas as pd
import pymysql


class Db_Mysql():
    # 获取Mysql连接
    def getMysqlConnect(self):
        host = '********'
        port = 3306
        user = '******'
        password = '******'
        database = 'mysql'
        connect = pymysql.connect(host=host
                                  , port=port
                                  , user=user
                                  , password=password
                                  , database=database
                                  , charset='utf8')  # 服务器名，账户，密码，数据库名,字符编码
        # 创建一个游标对象
        cursor = connect.cursor()
        return cursor, connect

    # 关闭Mysql连接
    def closeMysql(self, connect, cursor):
        cursor.close()
        connect.close()

    # 基于Mysql表解析配置信息
    def setMysqlTableInfos(self, cursor, tables):
        # 存储表信息
        table_infos = dict()
        # 获取列注释，作为excel中字段名称
        for sheet, table, bizdate in tables:
            cols_sql = '''
                       select `table_name`, `column_name`, column_comment
    	               from information_schema.columns 
                       where table_schema='{}' and table_name='{}';
                   '''.format(table.split('.')[0], table.split('.')[1])
            cursor.execute(cols_sql)
            cols = cursor.fetchall()
            col_comments = []
            for col in cols:
                col_comments.append(col[2])
            table_info = {
                'table': table,
                'cols': col_comments
            }
            table_infos['{}({})'.format(sheet, bizdate)] = table_info

        print('获取配置...', table_infos.keys())
        return table_infos

    # 获取Mysql数据
    def getMysqlData(self, cursor, table, cols):
        sql = 'select * from {};'.format(table)
        cursor.execute(sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=cols)
        # print(df)
        return df

    # Mysql运行
    def runMysql(self, tables):
        # 获取连接
        cursor, connect = self.getMysqlConnect()
        table_infos = self.setMysqlTableInfos(cursor, tables)
        # 存储数据
        df_maps = dict()
        # 获取每个表数据并添加到df_maps
        for name, table_info in table_infos.items():
            # 获取数据
            df = self.getMysqlData(cursor, table_info['table'], table_info['cols'])
            df_maps[name] = df
        # print(df_maps)
        return df_maps