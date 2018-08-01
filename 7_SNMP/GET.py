#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from pysnmp.hlapi import *

# varBinds是列表，列表中的每个元素的类型是ObjectType（该类型的对象表示MIB variable）
errorIndication, errorStatus, errorindex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('qytangro'),  # 配置community
           UdpTransportTarget(('10.1.1.253', 161)),  # 配置目的地址和端口号
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),  # 读取的OID
           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))  # 读取的OID
           )
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (
        errorStatus,
        errorindex and varBinds[int(errorindex) - 1][0] or '?'
    )
          )

for varBind in varBinds:
    print(varBind)  # 打印返回的结果！
