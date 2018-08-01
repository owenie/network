#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错
import re
from scapy.all import *

qyt_string = b''


def reset_tcp(pkt):
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


def telnet_monitor_callback(pkt):
    global qyt_string
    try:
        if pkt.getlayer(TCP).fields['dport'] == 23:
            if pkt.getlayer(Raw).fields['load'].decode():
                qyt_string = qyt_string + pkt.getlayer(Raw).fields['load']
    except Exception as e:
        #	#print(e)
        pass
    # print(qyt_string)
    if re.match(b'(.*\r\n.*)*sh.*\s+ver.*', qyt_string):
        reset_tcp(pkt)


PTKS = sniff(prn=telnet_monitor_callback, filter="tcp port 23 and ip host 10.1.1.253", store=1, timeout=15,
             iface='ens33')
wrpcap("temp.cap", PTKS)
print(qyt_string)
