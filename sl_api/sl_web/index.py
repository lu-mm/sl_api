#!/usr/bin/env python
#coding=utf-8
from flask import render_template

from sl_web import web_views


@web_views.route('/')
def index():
    return render_template('index.html')



@web_views.route('/login')
def login():
    return "登陆"