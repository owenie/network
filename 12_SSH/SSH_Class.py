#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import paramiko
import time
from Simple_SSH_Client import QYT_SSHClient_SingleCMD
from Adv_SSH_Client import QYT_SSHClient_MultiCMD

# def QYT_SSHClient_MultiCMD(ip, username, password, cmds):
#     ssh = paramiko.SSHClient()  # 创建SSH Client
#     ssh.load_system_host_keys()  # 加载系统SSH密钥
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
#     ssh.connect(ip, port=22, username=username, password=password, timeout=5, compress=True)  # SSH连接
#
#     chan = ssh.invoke_shell()  # 激活交互式shell
#     time.sleep(1)
#     x = chan.recv(2048).decode()  # 接收回显信息
#
#     for cmd in cmds:  # 读取命令
#         chan.send(cmd.encode())  # 执行命令，注意字串都需要编码为二进制字串
#         chan.send(b'\n')  # 一定要注意输入回车
#         time.sleep(2)  # 由于有些回显可能过长，所以可以考虑等待更长一些时间
#         x = chan.recv(40960).decode()  # 读取回显，有些回想可能过长，请把接收缓存调大
#         print(x)  # 打印回显
#
#     chan.close()  # 退出交互式shell
#     ssh.close()  # 退出ssh会话


class QYT_SSH():
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def MultiCMD(self, cmds):
        QYT_SSHClient_MultiCMD(self.ip, self.username, self.password, cmds)

    def SingleCMD(self, cmd):
        QYT_SSHClient_SingleCMD(self.ip, self.username, self.password, cmd)


if __name__ == '__main__':
    qyt_ssh_1 = QYT_SSH("10.1.1.253", "admin", "Cisc0123")
    #qyt_ssh_1.SingleCMD('show ver')
    qyt_ssh_1.MultiCMD(['term len 0', 'show ver','show ip inter brie'])
