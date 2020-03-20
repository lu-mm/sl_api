#!/usr/bin/env python
# -*- coding：utf-8 -*-
import json
import os
from assets.aliyun_ecs import EcsInfo
from utils.ext import api, mylog, db
from utils.settings import envs
from assets.ansible_mysql import Ansible_Hosts
from flask_restful import Resource
from flask import render_template

from assets import assets_view

class AliyunEcsList(Resource):
    def __init__(self):
        env = os.environ.get("FLASK_ENV") or "default"
        config = envs.get(env)
        access_key = config.access_key
        access_secret = config.access_secret
        region_id = config.region_id
        self._ecsInit=EcsInfo(access_key,access_secret,region_id)


    def get(self):
        """
        aliyun ecs list
        ---
        responses:
          200:
            description: aliyun ecs list

        """
        try:
            ecs_list = self._ecsInit.get_instance_info()
        except Exception as e:
            mylog().error(e)

        return json.loads(ecs_list)

api.add_resource(AliyunEcsList, '/assets/aliyun/hosts/list')


class AssetsList(Resource):
    def get(self):
        """
        List of valid assets
        ---
        responses:
          200:
            description: assets list

        """
        # def Task_All():
        #
        # 	try:
        # 		data=py_db.get_list(sql)
        # 	except Exception as e:
        # 		print(e)
        # 		return "error"
        # 	finally:
        # 		py_db.close()
        # 	return json.dumps(data,ensure_ascii=False)
        sql = "select name,fqdn,main_ip,vcpus,ram,disk_total,disk_free,is_active from hosts where is_active=0"
        try:
            db.connect()
            ret=db.get_list(sql)
        except Exception as e:
            pass
        finally:
            db.close()
        return json.loads(ret)
api.add_resource(AssetsList,'/assets/hosts/list')


class AssetsUpdate(Resource):

    def get(self):
        """assets update
        ---
        responses:
          200:
            description: assets update

        """
        ansible=Ansible_Hosts()
        try:
            ansible.ansible_html()
            ansible.ansibel_sql()
            status="success"
        except Exception as e:
            status="error"
        return {"status":status}

api.add_resource(AssetsUpdate,'/assets/hosts/update')




@assets_view.route('/index.html', methods=['GET'])
def Assets_views():
    return render_template("host.html")






