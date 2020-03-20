import json
import os

import pymysql

from utils.settings import envs


class SQLManager():
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()


    def connect(self):
        env = os.environ.get("FLASK_ENV") or "default"
        config = envs.get(env)
        databases_info = config.DATABASE

        self.connection = pymysql.connect(host=databases_info.get('host'),
                                          port=databases_info.get('port'),
                                          user=databases_info.get('user'),
                                          password=databases_info.get('password'),
                                          db=databases_info.get('db'),
                                          charset=databases_info.get('charset'),
                                          )

        self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询多条数据
    def get_list(self, sql, args=None):
        try:
            self.cursor.execute(sql, args)
            #fetchall获取查询结果的所有行。它返回所有行的元组的列表。如果没有记录来获取返回一个空列表。
            result = self.cursor.fetchall()
            return json.dumps(result,ensure_ascii=False)
        except Exception:
            raise

    # 查询单条数据
    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return json.dumps(result, ensure_ascii=False)

    # 执行单条SQL语句
    def moddify(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.connection.commit()

    # 执行多条SQL语句
    def multi_modify(self, sql, args=None):
        self.cursor.executemany(sql, args)
        self.connection.commit()

    # 创建单条记录的语句
    def create(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.connection.commit()
        last_id = self.cursor.lastrowid
        return last_id

    def sqlfile(self, sqlfile, args=None):
        sqlfile = sqlfile
        try:
            with open(sqlfile, 'r', encoding='utf-8') as f:
                file = f.read()
            sqlCommands = file.split(';')
            for command in sqlCommands:
                if command.isspace():
                    pass
                else:
                    try:
                        self.cursor.execute(command)
                    except Exception as msg:
                        raise
        except Exception as e:
            raise
        self.connection.commit()

    # 关闭数据库cursor和连接
    def close(self):
        self.cursor.close()
        self.connection.close()
