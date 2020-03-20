import json

from flask import request
from flask_restful import Resource

from my_ansible.AnsibleApi import AnsibleApi
from utils.ext import api



class CommandApi(Resource):
    def post(self):

        """
        shell command
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Product
              required:
                - command
                - host
              properties:
                command:
                  type: string
                  description: linux command.
                  default: "ls /tmp"
                host:
                  type: string
                  description: ansible host or groups.
                  default: "localhost"

        responses:
          200:
            description: The product inserted in the database
            content:
            application/json:
                schema:
                  $ref: '#/definitions/Product'
          500:
            description: 参数不对

        """

        # info = request.json
        try:
            host=request.json.get('host')
            command=request.json.get('command')
        except Exception as e:
            return {'student': None}, 500

        anisble = AnsibleApi()
        meg = anisble.runansible(host=host,command=command)
        return json.loads(meg)



api.add_resource(CommandApi,'/task/shell')




