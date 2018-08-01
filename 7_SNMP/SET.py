#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('qytangrw'),  # 写入Community
    cmdgen.UdpTransportTarget(('10.1.1.253', 161)),  # IP地址和端口号
    ('1.3.6.1.2.1.1.5.0', rfc1902.OctetString('SNMPv2R1'))  # OID和写入的内容，需要进行编码！
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (
        errorStatus.prettyPrint(),
        errorindex and varBinds[int(errorindex) - 1][0] or '?'
    )
          )
for name, val in varBinds:
    print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))  # 打印修改的结果
