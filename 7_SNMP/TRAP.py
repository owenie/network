#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api


def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):  # 处理Trap信息的函数
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))  # 提取版本信息
        if msgVer in api.protoModules:  # 如果版本兼容
            pMod = api.protoModules[msgVer]
        else:  # 如果版本不兼容，就打印错误
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),  # 对信息进行解码
        )
        print('Notification message from %s:%s: ' % (
            transportDomain, transportAddress  # 打印发送TRAP的源信息
        )
              )
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                print('Enterprise: %s' % (
                    pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                )
                      )
                print('Agent Address: %s' % (
                    pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                )
                      )
                print('Generic Trap: %s' % (
                    pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                )
                      )
                print('Specific Trap: %s' % (
                    pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                )
                      )
                print('Uptime: %s' % (
                    pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                )
                      )
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)
            print('Var-binds:')
            for x in varBinds:
                for x,y in x.items():
                    print(x,y)
    return wholeMsg


transportDispatcher = AsynsockDispatcher()  # 创建实例

transportDispatcher.registerRecvCbFun(cbFun)  # 调用处理Trap信息的函数

# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('10.1.1.80', 162))  # 绑定到本地地址与UDP/162号端口
)

transportDispatcher.jobStarted(1)  # 开始工作

try:
    # Dispatcher will never finish as job#1 never reaches zero
    transportDispatcher.runDispatcher()  # 运行
except:
    transportDispatcher.closeDispatcher()
    raise
