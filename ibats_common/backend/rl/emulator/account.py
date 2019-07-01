#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/6/28 17:08
@File    : account.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import numpy as np
import pandas as pd
from ibats_common.backend.rl.emulator.market import QuotesMarket


class Account(object):
    def __init__(self, md_df, data_factors):
        self.A = QuotesMarket(md_df, data_factors)

    def reset(self):
        self.buffer_reward = []
        self.buffer_value = []
        self.buffer_action = []
        self.buffer_cash = []
        return np.expand_dims(self.A.reset(), 0)

    def step(self, action):
        next_state, reward, done = self.A.step(action)

        self.buffer_action.append(action)
        self.buffer_reward.append(reward)
        self.buffer_value.append(self.A.total_value)
        self.buffer_cash.append(self.A.cash)
        return np.expand_dims(next_state, 0), reward, done

    def plot_data(self):
        df = pd.DataFrame([self.buffer_value, self.buffer_reward, self.buffer_cash, self.buffer_action]).T
        length = df.shape[0]
        df.index = self.A.data_close.index[:length]
        df.columns = ["value", "reward", "cash", "action"]
        return df


def _test_account():
    env = Account(data_quotes, data_fac)


if __name__ == "__main__":
    pass