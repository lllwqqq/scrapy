#!/usr/bin/python
# -*- coding: utf8 -*-

# 主配置
#######################################################################################
# 全局版本，debug为测试版，很多动作就是测试的样子
import collections

from base_config import *

# aes加密用串
g_aeskey = 'qwyumxQq73DKxDrGTW4zFkWCQWTHcrci'

# tornado安全cookie用加密串
g_cookie_secret_str = 'NMG4B4UtiT6ceQ6SC59yBLcjZyLycWbDCaw4rQ4rcvRvgVhcEVjKLDQHuWaDbiyK'

# 后台进程是否用gevent跑
# g_daemon_usegevent = True

# 缓存库使用模块
# redis
# memcache
g_xcache_type = 'memcache'

# 全局xcache开关
g_use_xcache = True

# 零时间设定
zerotime = '1970-01-01 00:00:00'

# 数据库相关配置
#######################################################################################
# 连接数分配方案：
# 计算程序见python AdminTools.py -n
if g_version == 'debug':
    # pg配置
    g_db_user = 'dbuser'
    g_db_password = '123kkk'
    g_db_host = '127.0.0.1'
    g_db_port = 5432
    g_db_database = 'xdmdb'
    g_db_async_maxconn = 33
    g_db_sync_maxconn = 10
    # xcache memcache连接
    g_memcache_server = '127.0.0.1:11211'

    # server_name配置
    g_cookie_domain = None  #


# 外网测试环境用，外网测试环境数据库
elif g_version == 'test':
    # pg配置
    g_db_user = 'dbuser'
    g_db_password = 'E4zhUejptQY4'
    g_db_host = 'rm-bp1p9545g92dbc4pn.pg.rds.aliyuncs.com'
    g_db_port = 3433
    g_db_database = 'xdmdb_5d5'
    g_db_async_maxconn = 10
    g_db_sync_maxconn = 10
    # xcache memcache连接
    g_memcache_server = '127.0.0.1:11211'

    g_cookie_domain = 'xiaoyuanzhao.com'

else:
    # pg配置
    g_db_user = 'dbuser'
    g_db_password = 'uGhPi2h7P6Q8'
    g_db_host = '10.56.7.8'
    g_db_port = 5432
    g_db_database = 'xdmdb'
    g_db_async_maxconn = 10
    g_db_sync_maxconn = 10
    # xcache memcache连接
    g_memcache_server = '127.0.0.1:11211'

    g_cookie_domain = None

g_memcache_pool_minsize = 5
g_memcache_pool_size = 20
######################################################################################

# 当前域名
# 第一个是主域名，第二个是测试域名
mydomains = ['www.shixiseng.com', 'toby.shixiseng.com']

# 图片服务器配置域名
##############################################################################

# 阿里云oss配置

if g_version == 'debug':
    g_oss_endpoint = "oss-cn-hangzhou.aliyuncs.com"
    g_opensearch_endpoint = 'http://opensearch-cn-hangzhou.aliyuncs.com'
    g_opensearch_index_name = 'shixiseng'  # shixisengtest
else:
    g_oss_endpoint = "oss-cn-hangzhou-internal.aliyuncs.com"
    g_opensearch_endpoint = 'http://intranet.opensearch-cn-hangzhou.aliyuncs.com'
    g_opensearch_index_name = 'shixiseng'

g_oss_keyid = "hTO9nvV5R56oJhOF"
g_oss_keysecret = "nMVG92dg1twJ5k0o3YnGeCQBoVfKXZ"
g_oss_bucket = 'sxsimg'

g_pic_server_host = 'www.sxsimg.com'
g_pic_server_uri = 'http://www.sxsimg.com/'

# 自建vsftpd的配置
# g_uploader_ftp_user = 'newuser'
# g_uploader_ftp_password = 'nwdm5&rAQi^6yBFn'

# 允许上传的文件类型
g_uploader_allow_type = (
    'application/pdf',
    'text/plain',
    'image/gif',
    'application/msword',
    'application/kswps',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'application/x-jpe',
    'image/jpg',
    'application/x-jpg',
    'image/png',
    'application/x-png',
    'application/vnd.ms-powerpoint',
    'application/x-ppt',
    'application/docx',
    'application/octet-stream'
)
# 需要原始状态保存的文件（图片一般要压缩，所以这里应该是pdf，doc这种，gif也是原始保存不压缩)
g_uploader_original_save_type = (
    'application/pdf',
    'text/plain',
    'image/gif',
    'application/msword',
    'application/kswps',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint',
    'application/x-ppt',
    'application/docx',
    'application/octet-stream',  # docx
)
# 最大允许5MB的图片
g_uploader_maxsize = 5120
# 图片最大宽度px
g_uploader_pic_max_width = 1920
# 图片预览图最大宽度px
g_uploader_pic_thumb_max_width = 320

# 状态中文
g_status_show = {
    'normal': '正常',
    'destroy': '已删',
    'delivered': '投递成功',
    'checked': '被查看',
    'notify': '通知面试',
    'freeze': '被冻结',
    'offline': '离线',
    'done': '已解决',
    'processing': '解决中',
    'request': '请求中',
    'uncheck': '未审核',
    'pass': '通过',
    'reject': '拒绝',
    'expired': '过期',
    'unactive': '未激活',
    'black': '拉黑',
    'sign': '申请',
    'obsolete': '已过时',
    'ongoing': '进行中',
    'submission': '待审中',
    'failed': '失败',
    'crecruit': '双选会',
    'read': '已读',
    'online': '上线',
    'update': '更新'
}
status_show = {
    'uncheck': '未推送',
    'abandon': '放弃',
    'normal': '已推送',
    'destroy': '已删除'
}
# 日志字段中文
g_log_show = {
    'effective_time': '截止日期',
    'refresh_time': '刷新日期',
    'pre_refresh': '预刷新',
    'intern': '职位'
}

# 实习僧管理员权限定义,显示顺序为这个设置的顺序
# 设置这个后，增加对应的handler即可在左侧显示出来
# 每条的定义为[显示名称，uri，图标class定义]
g_permissions = collections.OrderedDict()
g_permissions['media_manager'] = ['多媒体库', '/media/manager', 'fa fa-file-image-o']
g_permissions['cache_refresh'] = ['缓存刷新', '/cache/refresh', 'fa fa-refresh']
g_permissions['system_manager'] = ['系统管理', '/adminuser/manager', 'fa fa-cogs']
g_permissions['spider_manager'] = ['爬虫管理', '/spider/manager', 'fa fa-cogs']
g_permissions['cheat_room'] = ['聊天室', '/cheat/room', 'fa fa-cogs']
