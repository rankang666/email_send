## 项目名称
> 将odps/mysql/sqlserver查询的结果以邮件的方式发送


## 运行条件
> 列出运行该项目所必须的条件和相关依赖
>pip install pymysql (mysql)
>pip install pymssql (sqlserver)
>pip install pyodps (dataworks)
>pip install pandas 
>pip install easyemail （邮箱模块）
>smtplib(python内置模块,不需要安装)



## 运行说明
> 说明如何运行和使用你的项目，建议给出具体的步骤说明
> 运行脚本: python Email_Send.py
> 配置信息:需配置邮箱登录信息,邮件主题及收件人/抄送人信息
>         配置查询的表名,分区,保存文件路径
> 注意: 输出文件列名是基于对应表的列注释,自动解析生成


## 目录树说明
> └─email_send
    │  README.md -- 项目说明
    │
    ├─email_send
    │  │  Db_GetData.py -- 多种数据源统一处理
    │  │  Db_Mysql.py -- mysql数据获取处理
    │  │  Db_Odps.py -- odps数据获取处理
    │  │  Db_SqlServer.py -- sqlserver数据获取处理
    │  │  Email_Send.py -- 主文件,将数据获取和邮件发送整合在一起
    │  │  __init__.py
    │  │
    │  └─__pycache__
    └─email_utils
            EmailContent.py --邮件正文
            SendEmail.py -- 多种类型实现发送邮件
            __init__.py



## 技术架构
> python


## 协作者
> rk
