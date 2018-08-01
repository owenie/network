#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import pyshark


def get_tcp_stream(pcapfile, id):
    tcp_stream_pkt_list = []

    cap = pyshark.FileCapture(pcapfile, keep_packets=False)

    for pkt in cap:
        try:
            #print(str(pkt.tcp.stream))
            if str(pkt.tcp.stream) == str(id):
                tcp_stream_pkt_list.append(pkt)
        except:
            pass
    return tcp_stream_pkt_list


if __name__ == '__main__':
    #print(get_tcp_stream('dos.pcap', 193))
    i = 1
    for pkt in get_tcp_stream('dos.pcap', 10):
        print('='*30,i,'='*30)
        pkt.pretty_print()
        i += 1
