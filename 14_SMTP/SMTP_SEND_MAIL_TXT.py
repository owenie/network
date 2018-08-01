#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import smtplib, sys, email.utils


def qyt_smtp_sendmail(mailserver, username, password, From, To, Subj):
    Tos = To.split(';')  # 把多个邮件接受者通过';'分开
    Date = email.utils.formatdate()  # 格式化邮件时间
    # print(Date)
    text = ('From: %s\nTo: %s\nData: %s\nSubject: %s\n\n' % (From, To, Date, Subj))
    # print(text)
    server = smtplib.SMTP_SSL(mailserver,465)  # 连接邮件服务器
    server.login(username, password)  # 通过用户名和密码登录邮件服务器
    failed = server.sendmail(From, Tos, text)  # 发送邮件
    server.quit()  # 退出会话
    if failed:
        print('Falied recipients:', failed)  # 如果出现故障，打印故障原因！
    else:
        print('No errors.')  # 如果没有故障发生，打印‘No errors.’！
    print('Bye.')


if __name__ == '__main__':
    qyt_smtp_sendmail('smtp.qq.com', '3348326959@qq.com', 'mygmsrdptfuwcjbh', '3348326959@qq.com',
                       '3348326959@qq.com;collinsctk@qytang.com', 'This is a text only mail')
    # import getpass
    #
    # username = input('请输入用户名: ')
    # password = getpass.getpass('请输入密码: ')  # 读取密码，但是不回显！
    # qyt_smtp_sendmail('smtp.qq.com', username, password, username,
    #                   'collinsctk@qytang.com', 'This is a text only mail')
