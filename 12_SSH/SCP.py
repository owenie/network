#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import paramiko, os, sys, time


def ssh_scp_put(ip, user, password, local_file, remote_file, port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, user, password)
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)


def ssh_scp_get(ip, user, password, remote_file, local_file, port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, user, password)
    sftp = ssh.open_sftp()
    sftp.get(remote_file, local_file)


if __name__ == '__main__':
    #ssh_scp_put('10.1.1.80', 'root', 'Cisc0123', 'Adv_SSH_Client.py', 'Adv_SSH_Client.py', port=22)
    ssh_scp_get('10.1.1.80', 'root', 'Cisc0123', 'get-pip.py', 'get-pip.py', port=22)