# -*- coding: UTF-8 -*-
import json
import os
import subprocess

from utils.ext import db
from utils.ext import mylog
from utils.settings import envs




class Ansible_Hosts():
    def __init__(self):
        """
        ansible hosts --> mysql
        """
        env = os.environ.get("FLASK_ENV") or "default"
        config = envs.get(env)
        self.nodefile = config.ansible_node_file
        self.ansible_template=config.ansible_template
        self.hostfile = config.ansible_host_file
        self.sql_dir = config.ansible_host_sql
        self.hosts_html="templates/host.html"
        # self.sql_dir = "hosts.sql"
        # self.nodefile = "nodefile"

    def ansible_html(self):
        devnull = open(os.devnull, 'w')
        try:

            subprocess.call("rm -rf "+self.nodefile+" && ansible -i " + self.hostfile + " -m setup --tree " + self.nodefile + " all", shell=True,
                                 stdout=devnull,stdin=devnull,stderr=devnull, universal_newlines=True)
            subprocess.check_output("ansible-cmdb -i " + self.hostfile+" "+self.nodefile+" > " +self.hosts_html, shell=True,stderr = subprocess.STDOUT,universal_newlines=True)
            mylog().info("ansible最新信息已经更新到html")
        except subprocess.CalledProcessError as e:
            mylog().error(e.output)
            raise

    def ansibel_sql(self):

        try:
            ret=subprocess.check_output("ansible-cmdb -i " + self.hostfile + " --template="+self.ansible_template + " "+ self.nodefile + " > " +self.sql_dir,shell=True,stderr = subprocess.STDOUT,universal_newlines=True)
        except subprocess.CalledProcessError as e:
            mylog().error(e.output)
            raise
        try:
            db.connect()
            # sqlfiledir="my_ansible/"+self.sql_dir
            # list_nodefile="my_ansible/"+self.nodefile

            db.sqlfile(self.sql_dir)
            for files in os.listdir(self.nodefile):
                with open(self.nodefile +"/"+ files ,'r') as f:
                    load_dict =json.loads(f.read())
                    if "unreachable" in load_dict:
                        sql="update hosts set is_active=1 where name=%s"
                        db.moddify(sql,(files))
            mylog().info("ansible最新信息已经更新到数据库")
        except Exception as e:
            mylog().error(e)
            raise
        finally:
            db.close()