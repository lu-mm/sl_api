#!/bin/bash
#date:2020.01.03
#install sl_api
#version:1.1


dir=`pwd`
path=`echo $PATH`
gunicorn_path=`which gunicorn`
env=`echo $FLASK_ENV`


echo FLASK_ENV=$env > $dir/flaskenv


cat <<EOF > /etc/systemd/system/sl_api.service
[Unit]
Description=Gunicorn instance to serve sl_api
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$dir/sl_api
EnvironmentFile=-$dir/flaskenv
Environment=PATH=$path
ExecStart=$gunicorn_path --workers 3 --bind 0.0.0.0:5000 manager:app

[Install]
WantedBy=multi-user.target
EOF


systemctl daemon-reload
systemctl start sl_api
systemctl enable sl_api