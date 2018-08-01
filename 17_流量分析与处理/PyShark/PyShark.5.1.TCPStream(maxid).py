#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import pyshark


def get_max_id(pcapfile):
    cap = pyshark.FileCapture(pcapfile, keep_packets=False)

    sess_index = []  # to save stream indexes in an array

    for pkt in cap:
        try:
            sess_index.append(pkt.tcp.stream)
        except:
            pass

    if len(sess_index) == 0:
        max_index = 0
        print('No TCP Found')
    else:
        sess_index_int = [int(sid) for sid in sess_index]

    return max(sess_index_int)


if __name__ == '__main__':
    print(get_max_id('dos.pcap'))
