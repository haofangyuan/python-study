#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os

env_dist = os.environ

print(env_dist.get('JAVA_HOME'))
print(env_dist['JAVA_HOME'])
print(env_dist['path'])

# 设置只对此次操作起作用，并未修改系统中的变量
env_dist['JAVA_HOME'] = r'D:\Java\jdk1.7.0_03'
print(env_dist['JAVA_HOME'])
print(env_dist['path'])

# TODO 怎样永久设置？
