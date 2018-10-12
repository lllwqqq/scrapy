#!/usr/bin/python
# -*- coding: utf8 -*-
g_version = 'release'     # test, debug, release

# 是否打印sql语句
g_show_all_sql = False


# 是否加载本地的资源，True为加载本地，否则为加载oss上的
g_debug_source = True

# 是否自动加载html和py，tornado的autoreload，在不是debug的模式下自动重启服务器进程
g_server_autoreload = True