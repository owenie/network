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
import re


def findpcapdos(pcap_filename):
    pcap_file = rdpcap(pcap_filename)
    plist = pcap_file.res

    dos_dict = {}
    for packet in plist:
        try:
            if packet[0][2].fields['flags'] == 2:
                source_ip = packet[0][1].fields['src']
                destination_ip = packet[0][1].fields['dst']
                destination_port = packet[0][2].fields['dport']
                socket = source_ip, destination_ip, destination_port
                try:
                    dos_dict[socket]  # 判断是否有这个键值
                except:
                    dos_dict[socket] = 1  # 如果没有，就设置为1
                else:
                    dos_dict[socket] = dos_dict[socket] + 1  # 如果有就在原来值的基础之上加1
        except:
            pass
    for socket, num in dos_dict.items():
        if num > 3:
            print('DOS正在进行中，源为: ' + socket[0] + '目的为: ' + socket[1] + ' 目的端口为: ' + str(socket[2]) + ' 次数为: ' + str(num))


if __name__ == '__main__':
    findpcapdos("dos.pcap")
