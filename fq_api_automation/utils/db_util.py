# # -*- coding: utf-8 -*-
# """
# -------------------------------------------------
#    File Name：     lazyProperty
#    Description :
#    Author :        JHao
#    date：          2016/12/3
# -------------------------------------------------
#    Change Activity:
#                    2016/12/3:
# -------------------------------------------------
# """
#
# from config.logHandler import exception_decorator
# import pandas as pd
#
# import psycopg2
# from multiprocessing.dummy import Lock
#
# from utils.ini_util import read_ini
#
#
# data=read_ini.read_ini()["postgresql"]
# DB_CONF={
#     "host":data["POSTGRESQL_HOST"],
#     "port":int(data["POSTGRESQL_PORT"]),
#     "user":data["POSTGRESQL_USER"],
#     "password":data["POSTGRESQL_PASSWD"]
#
# }
#
# class DB():
#
#     #连接池对象
#
#     __pool = None
#
#     #多线程锁
#     _instance_lock = Lock()
#
#     #装实例化对象，相同参数的实例化共用一个实例化对象
#     arg ={}
#
#     dic = {
#         "PG":{"jdbc":psycopg2,"db_config":DB_CONF
#         #"GaussDB":{"jdbc":psycopg2,"db_config":conf.sqlserver_db_config
#                    }
#     }
#
#     def __init__(self,dbname,dbtype):
#         """
#         数据库构造函数，创建连接与游标
#         :param dbtype: sqlserver | PG| GaussDB
#         :param dbname : 数据库名
#         :param db_config:
#         """
#         self.jdbc = self.dic.get(dbtype).get('jdbc')
#         self.db_config = self.dic.get(dbtype).get('db_config')
#         self.db_config["db_name"]=dbname
#         self._conn = DB.__getConn(self.jdbc,self.db_config)
#
#     def __new__(cls, *args, **kwargs):
#         """
#         相同参数共用一个实例化对象
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         if str(args)+str(sorted(kwargs.items())) in DB.arg.keys():
#             return DB.arg.get(str(args)+str(sorted(kwargs.items())))
#         with cls._instance_lock:
#             DB.arg[str(args)+str(sorted(kwargs.items()))] = object.__new__(cls)
#             return DB.arg.get(str(args) + str(sorted(kwargs.items())))
#
#     @staticmethod
#     @exception_decorator()
#     def __getConn(jdbc,db_config):
#         # if DB.__pool is None:
#         #     __pool = PooledDB(creator=jdbc,mincached=10,maxcached=20,maxshared=10,maxconnections=200,blocking=True,maxusage=100,
#         #                       setsession=None,reset=True,**db_config
#         #                       )
#         #     return __pool
#         # else:
#             return DB.__pool
#
#     def get_pool_conn(self):
#         if not  self._conn:
#             self._conn = DB.__getConn(self.jdbc,self.db_config)
#         return self._conn.connection()
#
#     def begin(self):
#         """
#         开启事务
#         :return:
#         """
#         self._conn.connection().autocommit(0)
#
#     def end(self,option='commit'):
#         """
#         结束事务
#         :param option:
#         :return:
#         """
#         if option =='commit':
#             self._conn.connection().commit()
#         else:
#             self._conn.connection().rollback()
#
#     def dispose(self,isEnd=1):
#         """
#         释放连接池资源
#         :param isEnd:
#         :return:
#         """
#         if isEnd ==1:
#             self.end('commit')
#         else:
#             self.end('rollback')
#         self._conn.close()
#
#     def get_pd_data(self,sql):
#         return pd.read_sql(sql,self.get_pool_conn())
#
#
#     def exc_sql(self,sql):
#         """
#         执行sql
#         :return:
#         """
#         conn = self.get_pool_conn()
#         cursor = conn.cursor()
#         try:
#             cursor.execute(sql)
#             conn.commit()
#         except Exception:
#             #回滚
#             conn.commit()
#         finally:
#             conn.close()
#
#     def __del__(self):
#         self.dispose()
#
# if __name__ == '__main__':
#
#     M =DB(dbname='iotplat-security',dbtype="postgresql")
#     def db_select_send():
#         sql = "SELECT * FROM access_control"
#         conn = M.get_pool_conn()
#         cursor = conn.cursor()
#
#         cursor.execute(sql)
#         conn.commit()
#         row =cursor.fetchall()
#         data = pd.DataFrame(list(row))
#         cursor.close()
#         conn.close()
#         return data
#     db_select_send()
#     "****************"
#     sql = "SELECT * FROM access_control"
#     df = M.get_pd_data(sql)
#     print(df)
#     print(df.to_dict('index'))
#
#     print('dispose os OK')

#连接数据库
from turtledemo.penrose import inflatedart

import psycopg2
from psycopg2 import OperationalError

from utils.log_utils import logger
from utils.ini_util import read_ini

data=read_ini.read_ini()["postgresql"]
DB_CONF={
    "host":data["POSTGRESQL_HOST"],
    "port":int(data["POSTGRESQL_PORT"]),
    "user":data["POSTGRESQL_USER"],
    "password":data["POSTGRESQL_PASSWD"]
}

class PostgreSQLDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_user = DB_CONF['user']
        self.db_password = DB_CONF['password']
        self.db_host = DB_CONF['host']
        self.db_port = DB_CONF['port']
        self.connection = None

    def connect(self):
        """连接到PostgreSQL数据库"""
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            logger.info("成功连接到PostgreSQL数据库")
        except OperationalError as e:
            logger.error(f"无法连接到PostgreSQL数据库: {e}")

    def close_connection(self):
        """关闭数据库连接"""
        if self.connection is not None:
            self.connection.close()
            logger.info("PostgreSQL数据库连接已关闭")

    def execute_query(self, query):
        """执行SQL语句并返回结果

        Args:
            query (str): 要执行的SQL语句

        Returns:
            根据查询类型返回不同的结果。对于SELECT语句，返回查询结果；对于其他语句，返回None。
        """
        if self.connection is None:
            logger.info("数据库连接未建立")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()  # 对于非查询语句，提交事务

                # 检查是否为SELECT查询
                if query.upper().startswith('SELECT'):
                    result=cursor.fetchall()
                    logger.info(f"sql执行结果为{result}")
                    return result

                else:
                    # 对于INSERT、UPDATE、DELETE等非SELECT语句，返回None
                    logger.info("sql执行的是非查询语句")
                    return None

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"执行SQL时发生错误: {error}")
            return None

        # 使用示例


if __name__ == "__main__":
    db = PostgreSQLDatabase('iotplat-security')
    db.connect()

    # 执行SELECT查询
    query = "SELECT * FROM access_control"
    result = db.execute_query(query)
    print(result)
    db.close_connection()



