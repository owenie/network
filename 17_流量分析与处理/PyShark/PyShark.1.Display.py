#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import pyshark

#####################最原始操作,信息过量#####################
# cap = pyshark.FileCapture('dos.pcap')
#
# for pkt in cap:
#     print(pkt)
#     print(pkt.highest_layer)

#####################传一个函数,对pkt进行处理#####################
cap = pyshark.FileCapture('dos.pcap', keep_packets=False)


def print_highest_layer(pkt):
    print(pkt.highest_layer)


cap.apply_on_packets(print_highest_layer)

if __name__ == '__main__':
    pass
