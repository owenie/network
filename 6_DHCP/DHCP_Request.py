#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错
from scapy.all import *
import time


def DHCP_Request_Sendonly(ifname, options, wait_time=1):
    request = Ether(dst='ff:ff:ff:ff:ff:ff',
                    src=options['MAC'],
                    type=0x0800) / IP(src='0.0.0.0',
                                      dst='255.255.255.255') / UDP(dport=67, sport=68) / BOOTP(op=1,
                                                                                               chaddr=options[
                                                                                                          'client_id'] + b'\x00' * 10,
                                                                                               siaddr=options[
                                                                                                   'Server_IP'], ) / DHCP(
        options=[('message-type', 'request'),
                 ('server_id', options['Server_IP']),
                 ('requested_addr', options['requested_addr']),
                 ('client_id', b'\x01' + options['client_id']),
                 ('param_req_list', b'\x01\x06\x0f,\x03!\x96+'), ('end')])
    if wait_time != 0:
        time.sleep(wait_time)
        sendp(request, iface=ifname, verbose=False)
    else:
        sendp(request, iface=ifname, verbose=False)


if __name__ == '__main__':
    options = {'MAC': '00:0c:29:8d:5c:b6', 'Server_IP': '202.100.1.168', 'requested_addr': '202.100.1.1',
               'client_id': b'\x00\x0c)\x8d\\\xb6'}
    DHCP_Request_Sendonly('ens33', options)
