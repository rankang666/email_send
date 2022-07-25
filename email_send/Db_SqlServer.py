#!/usr/bin/env python
# encoding: utf-8
'''
@Time: 2022/7/20 20:26
@Project: mmb 
@File: Db_Sqlserver.py
@Author: rk
@Software: pycharm
@Desc:
'''
import pandas as pd
import pymssql


class Db_SqlServer():
    # 获取SQLServer连接
    def getSqlserverConnect(self):
        host = '********'
        port = '****'
        user = '******'
        password = '******'
        database = '***'
        connect = pymssql.connect(host=host
                                  , port=port
                                  , user=user
                                  , password=password
                                  , database=database
                                  , charset='utf8')  # 服务器名，账户，密码，数据库名,字符编码
        # 创建一个游标对象
        cursor = connect.cursor()
        return cursor, connect

    # 关闭SQLserver连接
    def closeSqlserver(self, connect, cursor):
        cursor.close()
        connect.close()

    # 基于sqlserver表解析配置信息
    def setSqlserverTableInfos(self, cursor, tables):
        # 存储表信息
        table_infos = dict()
        # 获取列注释，作为excel中字段名称
        for sheet, table, bizdate in tables:
            cols_sql = '''
                select a.name, b.name, c.value 
                from dbo.sysobjects a 
                left join dbo.syscolumns b 
                on a.id = b.id 
                left join sys.extended_properties c 
                on a.id = c.major_id AND b.colid = c.minor_id  
                where a.name = '{}'
            '''.format(table.split('.')[1])
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


    # 获取SQLserver数据
    def getSqlserverData(self, cursor, table, cols):
        sql = 'select * from {};'.format(table)
        cursor.execute(sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=cols)
        # print(df)
        return df


    # sqlserver运行
    def runSqlserver(self,tables):
        # 获取连接
        cursor, connect = self.getSqlserverConnect()
        table_infos = self.setSqlserverTableInfos(cursor, tables)
        # 存储数据
        df_maps = dict()
        # 获取每个表数据并添加到df_maps
        for name, table_info in table_infos.items():
            # 获取数据
            df = self.getSqlserverData(cursor, table_info['table'],table_info['cols'])
            df_maps[name] = df
        return df_maps