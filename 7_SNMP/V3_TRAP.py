#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
#from sendmail import sendTrapInfo
import sys
import re

# Create SNMP engine with autogenernated engineID and pre-bound
snmpEngine = engine.SnmpEngine()

config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('10.1.1.80', 162))
)

#Callback function for receiving notifications
def cbFun(snmpEngine,
          stateReference,
          contextEngineId, contextName,
          varBinds,
          cbCtx):
#    print('Notification received, ContextEngineId "%s", ContextName "%s"' % (
#        contextEngineId.prettyPrint(), contextName.prettyPrint()
#        )
#    )
    for name, val in varBinds:
        # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        # ============================Trap 信息处理方法===================================

        # ============================link up / link down===============================
        # snmp-server enable traps snmp linkdown linkup
        if '1.3.6.1.6.3.1.1.4.1.0' in name.prettyPrint() and '1.3.6.1.6.3.1.1.5.3' in val.prettyPrint():
            state = 'Down'
        elif '1.3.6.1.6.3.1.1.4.1.0' in name.prettyPrint() and '1.3.6.1.6.3.1.1.5.4' in val.prettyPrint():
                state = 'UP'

        if '1.3.6.1.2.1.2.2.1.2.3' in name.prettyPrint():
            print('*' * 20 + '接口状态' + '*' * 20)
            print('%s change state to %s' % (val.prettyPrint(), state))

        # ============================Enter / Exit Configure Mode=========================
        # snmp-server enable traps config
        if '1.3.6.1.6.3.1.1.4.1.0' in name.prettyPrint():
            if '1.3.6.1.4.1.9.9.43.2.0.1' in val.prettyPrint():
                print('*' * 20 + '配置模式改变' + '*' * 20)
                print('Enter Configure Mode!!!')
            elif '1.3.6.1.4.1.9.9.43.2.0.2' in val.prettyPrint():
                print('*' * 20 + '配置模式改变' + '*' * 20)
                print('Exit Configure Mode!!!')

        # ============================CPU================================================
        # IOS-XE 现在并不能主动发送Trap,但是激活snmp-server enable traps syslog,可以把Console log发过去
        if '1.3.6.1.4.1.9.9.41.1.2.3.1.4.' in name.prettyPrint():
            if 'CPU' in val.prettyPrint():
                cpu_state = val.prettyPrint()
        elif '1.3.6.1.4.1.9.9.41.1.2.3.1.5.' in name.prettyPrint():
            if 'CPU' in val.prettyPrint():
                print('*'*20 + cpu_state + '*'*20)
                print(val.prettyPrint())


def snmpv3_trap(user='',hash_meth=None,hash_key=None,cry_meth=None,cry_key=None,engineid=''):
    #usmHMACMD5AuthProtocol - MD5 hashing
    #usmHMACSHAAuthProtocol - SHA hashing
    #usmNoAuthProtocol - no authentication
    #usmDESPrivProtocol - DES encryption
    #usm3DESEDEPrivProtocol - triple-DES encryption
    #usmAesCfb128Protocol - AES encryption, 128-bit
    #usmAesCfb192Protocol - AES encryption, 192-bit
    #usmAesCfb256Protocol - AES encryption, 256-bit
    #usmNoPrivProtocol - no encryption
    hashval = None
    cryval = None

    #NoAuthNoPriv
    if hash_meth == None and cry_meth == None:
        hashval = config.usmNoAuthProtocol
        cryval = config.usmNoPrivProtocol
    #AuthNoPriv
    elif hash_meth != None and cry_meth == None:
        if hash_meth == 'md5':
            hashval = config.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = config.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
        cryval = config.usmNoPrivProtocol
    #AuthPriv
    elif hash_meth != None and cry_meth != None:
        if hash_meth == 'md5':
            hashval = config.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = config.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
        if cry_meth == '3des':
            cryval = config.usm3DESEDEPrivProtocol
        elif cry_meth == 'des':
            cryval = config.usmDESPrivProtocol
        elif cry_meth == 'aes128':
            cryval = config.usmAesCfb128Protocol
        elif cry_meth == 'aes192':
            cryval = config.usmAesCfb192Protocol
        elif cry_meth == 'aes256':
            cryval = config.usmAesCfb256Protocol
        else:
            print('加密算法必须是3des, des, aes128, aes192 or aes256 !')
            return
    #提供的参数不符合标准时给出提示
    else:
        print('三种USM: NoAuthNoPriv, AuthNoPriv, AuthPriv.。请选择其中一种。')
        return

    # SNMPv3/USM setup
    # user: usr-md5-des, auth: MD5, priv DES, contextEngineId: 8000000001020304
    # this USM entry is used for TRAP receiving purposes
    config.addV3User(
        snmpEngine, user,
        hashval, hash_key,
        cryval, cry_key,
        contextEngineId=v2c.OctetString(hexValue=engineid)
    )

    # Register SNMP Application at the SNMP engine
    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish

    # Run I/O dispatcher which would receive queries and send confirmations
    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise

if __name__ == '__main__':
    snmpv3_trap('qytanguser', 'sha', 'Cisc0123', 'des', 'Cisc0123', '800000090300005056AB4D19')
    # try:
    #     user = sys.argv[1]
    #     hm = sys.argv[2]
    #     hk = sys.argv[3]
    #     cm = sys.argv[4]
    #     ck = sys.argv[5]
    #     engineid = sys.argv[6]
    #     snmpv3_trap(user,hm,hk,cm,ck,engineid)
    # except:
    #     print('参数设置应该如下:')
    #     print('python3 mytrap.py 用户名 认证算法 认证密钥 加密算法 加密密钥 engineID')
    #     print('认证算法支持md5和sha')
    #     print('加密算法支持3des, des, aes128, aes192, aes256')
    #     print('例如：')
    #     print('sudo python3 mytrap.py user1 sha Cisc0123 des Cisc0123 800000090300CA011B280000')