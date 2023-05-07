# coding=utf-8
# 导入所需库
import pandas as pd


def data_preprocessing():
    # 读取本地的 CSV 文件
    total_zcfz_df = pd.read_csv('./data/资产负债表.csv')
    total_lrb_df = pd.read_csv('./data/利润表.csv')
    total_xjll_df = pd.read_csv('./data/现金流量表.csv')

    # 设置索引
    total_zcfz_df = total_zcfz_df.set_index(['公告日期', '股票代码'])
    total_lrb_df = total_lrb_df.set_index(['公告日期', '股票代码'])
    total_xjll_df = total_xjll_df.set_index(['公告日期', '股票代码'])

    # 数据清洗：去重
    total_zcfz_df = total_zcfz_df.drop_duplicates()
    total_lrb_df = total_lrb_df.drop_duplicates()
    total_xjll_df = total_xjll_df.drop_duplicates()

    # 计算同期资产、同期权益后合并数据
    total_zcfz_df['同期资产'] = total_zcfz_df['总资产'].unstack('股票代码').shift(1).stack('股票代码')
    total_zcfz_df['同期权益'] = total_zcfz_df['所有者权益'].unstack('股票代码').shift(1).stack('股票代码')

    # 合并数据
    total_df = pd.concat([total_zcfz_df, total_lrb_df, total_xjll_df], axis=1)

    # 计算净资产收益率、利润率、资产周转率、权益乘数
    total_df['净资产收益率'] = total_df['净利润'] / (total_df['所有者权益'] + total_df['同期权益']) * 2
    total_df['利润率'] = total_df['净利润'] / total_df['营业收入']
    total_df['资产周转率'] = total_df['营业收入'] / (total_df['总资产'] + total_df['同期资产']) * 2
    total_df['权益乘数'] = total_df['总资产'] / total_df['所有者权益']

    # 计算毛利润、毛利率、净利率
    total_df['毛利润'] = total_df['营业收入'] - total_df['营业成本']
    total_df['毛利率'] = total_df['毛利润'] / total_df['营业收入']
    total_df['净利率'] = total_df['净利润'] / total_df['营业收入']

    # 计算流动比率、速动比率、资产负债率、资产负债率（不含预收款）
    total_df['流动资产'] = total_df['货币资金'] + total_df['应收账款'] + total_df['存货']
    total_df['流动负债'] = total_df['应付账款'] + total_df['预收账款']
    total_df['流动比率'] = total_df['流动资产'] / total_df['流动负债']
    total_df['速动比率'] = (total_df['流动资产'] - total_df['存货']) / total_df['流动负债']
    total_df['资产负债率'] = total_df['总负债'] / total_df['总资产']
    total_df['资产负债率（不含预收款）'] = (total_df['总负债'] - total_df['预收账款']) / total_df['总资产']

    # 去除重复列
    total_df = total_df.loc[:, ~total_df.columns.duplicated()]

    # 去除净资产收益率缺失值
    total_df = total_df.dropna(subset=['净资产收益率'], how='all')

    total_df = total_df.reset_index(level='公告日期')
    total_df = total_df.reset_index(level='股票代码')

    # 处理缺失值
    total_df = total_df.dropna(subset=['净资产收益率'], how='all')
    total_df.fillna(method='ffill', inplace=True)

    # 处理异常值
    total_df = total_df[(total_df['净资产收益率'] > 0) & (total_df['净资产收益率'] < 1)]
    total_df = total_df[(total_df['利润率'] > 0) & (total_df['利润率'] < 1)]
    total_df = total_df[(total_df['资产周转率'] > 0) & (total_df['资产周转率'] < 1)]
    total_df = total_df[(total_df['权益乘数'] > 0) & (total_df['权益乘数'] < 10)]

    # 返回数据
    return total_df
