#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp
import sys
reload(sys)
sys.setdefaultencoding('utf8')
@resource_reference{"brokerLoad_dp_to_sr_util.py"}
dp_to_sr_util = imp.load_source('brokerLoad_dp_to_sr_util', 'brokerLoad_dp_to_sr_util.py')

"""
    提交同步dp外表数据到SR表,目前有以下限制:
    1、仅支持DP的ORC外表
    2、仅支持同名字段同步，不支持衍生字段
    3、如果DP表是分区表,仅支持单分区字段表同步
    4、如果SR表是分区表,要求源DP表也需要是分区表并且SR表与DP表分区字段一致
    5、如果SR表是非分区表，如果每日同步的数据涉及到源数据被删除，需要dp离线将删除的数据处理掉(该条删除记录的值设置为空)
    参数列表如下:
    sr_instance_name: sr集群名称,不清楚可以咨询数据平台组
    dp_full_table: dp表名称,格式:dp库.dp表
    sr_full_table: starrocks表名称,格式:starrocks库.starrocks表
    dp_partition: dp分区 格式:分区字段=分区值(例如:ds=20240905),当dp表是分区表时存在
    sync_sr_table_column_list: 需要同步的sr表的字段列表，如果该字段为空,则同步SR表全部字段,格式:多个字段以逗号分割
    *****schedule_type****: 调度类型,默认为DAY,值:DAILY:按日调度,HOURLY:按照小时调度,MINUTELY:按照分钟调度,MANUAL:手工执行,MONTHLY:按月调度
    retry_times: 重试次数,默认为3
    retry_minutes: 重试间隔分钟数,默认为5
    retry_expire_datetime: 重试过期时间,默认为None
    """
dp_to_sr_util.submit_dp_to_sr_sync(sr_instance_name="${instance}",
                                   dp_full_table="${dp}",
                                   sr_full_table="${sr}",
                                   dp_partition="${partition}",
                                   sync_sr_table_column_list="${columns}",
                                   schedule_type="MANUAL")