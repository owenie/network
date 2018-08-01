#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import pyshark

pkt_list = []

cap = pyshark.FileCapture('dos.pcap', keep_packets=False, display_filter='http')

#pkt
#['__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_packet_string', 'captured_length', 'eth', 'frame_info', 'get_multiple_layers', 'get_raw_packet', 'highest_layer', 'http', 'interface_captured', 'ip', 'layers', 'length', 'number', 'pretty_print', 'show', 'sniff_time', 'sniff_timestamp', 'tcp', 'transport_layer']
#ip
#['', 'DATA_LAYER', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_all_fields', '_field_prefix', '_get_all_field_lines', '_get_all_fields_with_alternates', '_get_field_or_layer_repr', '_get_field_repr', '_layer_name', '_sanitize_field_name', 'addr', 'checksum', 'checksum_status', 'dsfield', 'dsfield_dscp', 'dsfield_ecn', 'dst', 'dst_host', 'field_names', 'flags', 'flags_df', 'flags_mf', 'flags_rb', 'frag_offset', 'get', 'get_field', 'get_field_by_showname', 'get_field_value', 'hdr_len', 'host', 'id', 'layer_name', 'len', 'pretty_print', 'proto', 'raw_mode', 'src', 'src_host', 'ttl', 'version']
#tcp
#['DATA_LAYER', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_all_fields', '_field_prefix', '_get_all_field_lines', '_get_all_fields_with_alternates', '_get_field_or_layer_repr', '_get_field_repr', '_layer_name', '_sanitize_field_name', 'ack', 'analysis', 'analysis_bytes_in_flight', 'analysis_initial_rtt', 'analysis_push_bytes_sent', 'checksum', 'checksum_status', 'dstport', 'field_names', 'flags', 'flags_ack', 'flags_cwr', 'flags_ecn', 'flags_fin', 'flags_ns', 'flags_push', 'flags_res', 'flags_reset', 'flags_str', 'flags_syn', 'flags_urg', 'get', 'get_field', 'get_field_by_showname', 'get_field_value', 'hdr_len', 'layer_name', 'len', 'nxtseq', 'payload', 'port', 'pretty_print', 'raw_mode', 'seq', 'srcport', 'stream', 'urgent_pointer', 'window_size', 'window_size_scalefactor', 'window_size_value']
#http
#['', 'DATA_LAYER', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_all_fields', '_field_prefix', '_get_all_field_lines', '_get_all_fields_with_alternates', '_get_field_or_layer_repr', '_get_field_repr', '_layer_name', '_sanitize_field_name', '_ws_expert', '_ws_expert_group', '_ws_expert_message', '_ws_expert_severity', 'accept', 'accept_encoding', 'accept_language', 'chat', 'connection', 'cookie', 'cookie_pair', 'field_names', 'get', 'get_field', 'get_field_by_showname', 'get_field_value', 'host', 'layer_name', 'pretty_print', 'raw_mode', 'request', 'request_full_uri', 'request_line', 'request_method', 'request_number', 'request_uri', 'request_uri_path', 'request_uri_query', 'request_uri_query_parameter', 'request_version', 'user_agent']

url_dict = {}

# def print_highest_layer(pkt):
#     try:
#         counts = url_dict.get((pkt.http.request_method,pkt.http.host),0)
#         counts += 1
#         url_dict[(pkt.http.request_method,pkt.http.host)] = counts
#     except:
#         pass


def print_highest_layer(pkt):
    try:
        host_list = pkt.http.host.split('.')
        if len(host_list[-1]) == 2:
            host = host_list[-3] + '.' + host_list[-2] + '.' + host_list[-1]
        elif len(host_list[-1]) == 3:
            host = host_list[-2] + '.' + host_list[-1]
        else:
            next

        counts = url_dict.get((pkt.http.request_method,host),0)
        counts += 1
        url_dict[(pkt.http.request_method,host)] = counts
    except:
        pass

cap.apply_on_packets(print_highest_layer)

#print(url_dict)

# for key, value in url_dict.items():
#     print(key[0], key[1], value)

#排序
# f = zip(url_dict.values(),url_dict.keys())
#
# f = sorted(f)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    url = []
    hits = []
    for x,y in url_dict.items():
        url.append(x[1])
        hits.append(y)

    # plt.bar(application,data,width = 0.5)

    #color_list = ['r', 'k', '0.5', '#FF00FF']

    # 灰度
    # HTML颜色

    plt.barh(url, hits, height=0.5)

    ###########################添加注释###################################
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.title('站点访问量统计')  # 主题
    plt.xlabel('访问数量')  # X轴注释
    plt.ylabel('站点')  # Y轴注释
    ###########################添加注释###################################

    plt.show()
