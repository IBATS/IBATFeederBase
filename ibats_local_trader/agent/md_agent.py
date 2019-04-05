#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/20 19:53
@File    : md_agent.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import time
from ibats_common.md import MdAgentBase, md_agent
from ibats_common.common import PeriodType, RunMode, ExchangeName
import pandas as pd


class MdAgentPub(MdAgentBase):

    def __init__(self, instrument_id_list, md_period: PeriodType, exchange_name, file_path, agent_name=None,
                 init_load_md_count=None, init_md_date_from=None, init_md_date_to=None, **kwargs):
        MdAgentBase.__init__(
            self, instrument_id_list, md_period, exchange_name, agent_name=agent_name,
            init_load_md_count=init_load_md_count, init_md_date_from=init_md_date_from,
            init_md_date_to=init_md_date_to, **kwargs)
        self.file_path = file_path
        if 'datetime_key' in kwargs:
            self.datetime_key = kwargs['datetime_key']
            self.date_key = None
            self.time_key = None
        else:
            self.datetime_key = None
            self.date_key = kwargs['date_key']
            self.time_key = kwargs['time_key']
        if 'microseconds_key' in kwargs:
            self.microseconds_key = kwargs['microseconds_key']
        else:
            self.microseconds_key = None

        self.factors = kwargs['factors'] if 'factors' in kwargs else None

    def load_history(self, date_from=None, date_to=None, load_md_count=None) -> (pd.DataFrame, dict):
        """
        从文件中加载历史数据
        :param date_from: None代表沿用类的 init_md_date_from 属性
        :param date_to: None代表沿用类的 init_md_date_from 属性
        :param load_md_count: 0 代表不限制，None代表沿用类的 init_load_md_count 属性，其他数字代表相应的最大加载条数
        :return: md_df 或者
         ret_data {
            'md_df': md_df, 'datetime_key': 'ts_start',
            'date_key': **, 'time_key': **, 'microseconds_key': **
            }
        """
        # 如果 init_md_date_from 以及 init_md_date_to 为空，则不加载历史数据
        if self.init_md_date_from is None and self.init_md_date_to is None:
            ret_data = {'md_df': None, 'datetime_key': self.datetime_key, 'date_key': self.date_key,
                        'time_key': self.time_key, 'microseconds_key': self.microseconds_key}
            return ret_data

        # 加载历史数据
        self.logger.debug("加载历史数据 %s", self.file_path)
        date_col_name_set = {self.datetime_key, self.date_key, self.timestamp_key}
        if None in date_col_name_set:
            date_col_name_set.remove(None)
        md_df = pd.read_csv(self.file_path, parse_dates=list(date_col_name_set))
        # self.md_df = md_df
        ret_data = {'md_df': md_df, 'datetime_key': self.datetime_key, 'date_key': self.date_key,
                    'time_key': self.time_key, 'microseconds_key': self.microseconds_key,
                    'symbol_key': self.symbol_key, 'close_key': 'close'}
        return ret_data


@md_agent(RunMode.Backtest, ExchangeName.LocalFile, is_default=False)
class MdAgentBacktest(MdAgentPub):

    def __init__(self, **kwargs):
        MdAgentPub.__init__(self, **kwargs)
        self.timeout = 1
        self.timestamp_key = kwargs['timestamp_key'] if 'timestamp_key' in kwargs else self.datetime_key
        self.symbol_key = kwargs['symbol_key']
        self.close_key = kwargs['close_key'] if 'close_key' in kwargs else 'close'

    def connect(self):
        """链接redis、初始化历史数据"""
        pass

    def release(self):
        """释放channel资源"""
        pass

    def run(self):
        """启动多线程获取MD"""
        if not self.keep_running:
            self.keep_running = True
            while self.keep_running:
                time.sleep(self.timeout)
            else:
                self.logger.info('%s job finished', self.name)
