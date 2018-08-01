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


def findpcapuri(pcap_filename, host_regex):
    pcap_file = rdpcap(pcap_filename)
    plist = pcap_file.res
    for packet in plist:
        try:
            if packet[0][2].fields['dport'] == 80:
                http_request = packet[0][3].fields['load'].split()
                # print(http_request)
                Host_location = http_request.index(b'Host:') + 1
                Host = http_request[Host_location]
                Host_ACSII = Host.decode()
                if re.search(host_regex, Host_ACSII):
                    URI_location = http_request.index(b'GET') + 1
                    User_Agent_location = http_request.index(b'User-Agent:') + 1
                    URI = http_request[URI_location]
                    User_Agent = http_request[User_Agent_location]
                    print('====================================================================')
                    print(b'URI: ' + URI)
                    print(b'Host: ' + Host)
                    print(b'User_Agent: ' + User_Agent)
        except:
            pass


if __name__ == '__main__':
    findpcapuri("dos.pcap", 'sina\.com\.cn')
