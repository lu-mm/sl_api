#!/usr/bin/env python
#coding=utf-8
#encoding: utf-8

import json
import configparser
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from flask import session

from utils.ext import db
from sqlalchemy.dialects.mysql import insert
from utils.web_log import _LogFactory


class EcsInfo():
    def __init__(self,access_key,access_secret,region_id):
        """
        1.传入账户信息
        2.创建客户端连接
        3.阿里云所有ecs服务器的详细信息列表
        4.服务器同步
        """
        self.access_key = access_key
        self.access_secret = access_secret
        self.region_id=region_id
        self._request = DescribeInstancesRequest()
        self._request.set_accept_format('json')
        self._request.set_PageNumber(1)
        self._request.set_PageSize(100)
        self._connection = AcsClient(self.access_key, self.access_secret, region_id=self.region_id)
        self.aliyun_log = _LogFactory.get_logger('LOGGER')

    def get_instance_info(self):
        """

        :return: ecs list
        """

        self._server_list = []
        val = 1
        page_number = 1
        while val==1:
            self._request.set_PageNumber(page_number)
            try:
                response = self._connection.do_action_with_exception(self._request)
                # self.aliyun_log.info(msg="aliyun连接成功")
            except Exception as e:
                self.aliyun_log.error(msg=e)
                return "阿里云连接失败，请查看日志"

            response_data = json.loads(str(response, encoding='utf-8'))

            ret = response_data['Instances']['Instance']

            for i in ret:
                asset_data = {}
                asset_data['hostname'] = i.get('InstanceId')
                asset_data['remarks'] = i.get('InstanceName')
                # asset_data['region'] = i.get('ZoneId')
                # asset_data['instance_id'] = i.get('InstanceId')
                # asset_data['instance_type'] = i.get('InstanceType')
                asset_data['status'] = i.get('Status')
                asset_data['cpu'] = i.get('Cpu')
                asset_data['memory'] = i.get('Memory')
                # 单位换算G
                # asset_data['memory'] = str(int(i.get('Memory'))/1024) + 'G'
                # 内网IP
                try:
                    # VPC里面内网IP
                    asset_data['private_ip'] = i['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
                except (KeyError, IndexError):
                    # 非VPC里面获取内网IP
                    asset_data['private_ip'] = i['InnerIpAddress']['IpAddress'][0]

                # 公网IP/弹性IP
                try:
                    asset_data['public_ip'] = i['PublicIpAddress']['IpAddress'][0]
                except(KeyError, IndexError):
                    asset_data['public_ip'] = i['EipAddress']['IpAddress']
                except Exception:
                    asset_data['public_ip'] = asset_data['private_ip']
                asset_data['os_name'] = i.get('OSName')
                self._server_list.append(asset_data)


            if response_data['Instances']['Instance']:
                val = 2
            else:
                page_number += 1

        return  json.dumps(self._server_list,ensure_ascii=False)

    # def sync_instance(self):
    #
    #     insert_smt=insert(Aliun_ECS).values(self._server_list)
    #     on_duplicate_key_stmt = insert_smt.on_duplicate_key_update(
    #         hostname=insert_smt.inserted.hostname
    #     )
    #     try:
    #         db.execute(on_duplicate_key_stmt)
    #         db.commit()
    #     except Exception as e:
    #         return "error"


if __name__ == "__main__":
    pass
