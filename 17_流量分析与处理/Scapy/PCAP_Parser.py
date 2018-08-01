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


def pcap_parser(filename, keyword):
    pkts = rdpcap(filename)
    return_pkts_list = []  # 返回匹配数据包的清单！
    for pkt in pkts.res:
        try:
            pkt_load = pkt.getlayer('Raw').fields['load'].decode().strip()  # 提取负载内容
            re_keyword = '.*' + keyword + '.*'
            # 如果负载内容匹配，并且源端口为23，把数据包添加到return_pkts_list
            if re.match(re_keyword, pkt_load) and pkt.getlayer('TCP').fields['sport'] == 23:
                return_pkts_list.append(pkt)
        except:
            pass
    return return_pkts_list  # 返回匹配数据包的清单！


if __name__ == "__main__":
    pkts = pcap_parser("login_invalid.pcap", 'invalid')
    i = 1
    for pkt in pkts:
        print('==================第' + str(i) + "个包==================")
        pkt.show()
        i += 1
