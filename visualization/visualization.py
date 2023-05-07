# coding=utf-8
# 导入所需库
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def visualize_data(total_df, stock_code):
    # 询问用户要分析近几年的数据
    while True:
        years = input('请选择要分析近几年的数据（输入数字，如输入3则分析最近3年的数据，最多可以选择11年）：')
        if not years.isdigit() or int(years) < 1 or int(years) > 11:
            print('输入不合法，请重新输入')
        else:
            break

    # 根据用户选择的年数生成报告日期列表
    current_year = 2022
    report_date_list = [f"{year}-12-31" for year in range(current_year - int(years) + 1, current_year + 1)]
    print(f"你选择的数据时间段为{report_date_list[-1][:4]}年到{report_date_list[0][:4]}年")

    # 将年份列转换为datetime类型
    total_df['公告日期'] = pd.to_datetime(total_df['公告日期'])

    # 选择分析年份
    analysis_years = int(years)

    # 获取最近analysis_years年的年份
    recent_years = pd.date_range(end=pd.Timestamp.today(), periods=analysis_years, freq='Y').year

    # 筛选total_df，只保留最近analysis_years年的数据
    total_df = total_df[total_df['公告日期'].dt.year.isin(recent_years)]

    # 设置日期
    total_df = total_df.copy()
    total_df['公告日期'] = total_df['公告日期'].dt.strftime('%Y-%m-%d')

    # 1.企业经营总览
    stock_name = total_df[total_df['股票代码'] == stock_code]['股票简称'].values[0]

    # 选择对应股票的数据进行可视化
    analysis_df = total_df[total_df['股票代码'] == stock_code].copy()

    # 获取对应股票的行业名称
    industry_name = total_df[total_df['股票代码'] == stock_code]['行业名称'].values[0]

    # 选择同一行业的所有股票的数据进行可视化
    industry_df = total_df[total_df['行业名称'] == industry_name].copy()

    # 设置颜色
    color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # 可视化企业经营总览
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # 绘制总资产和总负债的堆积柱状图
    analysis_df.plot(x='公告日期', y=['总资产', '总负债'], kind='bar', stacked=True, ax=ax1, color=color_list[:2])
    ax1.set_xlabel('公告日期')
    ax1.set_ylabel('金额（元）')
    ax1.set_title(stock_name + '经营总览')
    ax1.legend(['总资产', '总负债'], loc='upper left')

    # 绘制其他指标的折线图
    analysis_df.plot(x='公告日期', y=['固定资产', '货币资金', '应收账款', '存货', '应付账款', '预收账款', '所有者权益', '营业利润', '净利润'], ax=ax2,
                     color=['#d62728', '#2ca02c', '#9467bd', '#ff7f0e', '#1f77b4', '#8c564b', '#e377c2', '#7f7f7f',
                            '#bcbd22'])
    ax2.set_ylabel('金额（元）')
    ax2.legend(['固定资产', '货币资金', '应收账款', '存货', '应付账款', '预收账款', '所有者权益', '营业利润', '净利润'], loc='upper right')
    ax1.grid(False)
    ax2.grid(False)

    # 2.偿债能力
    # 偿债能力
    fig2, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # 绘制资产负债率的折线图
    analysis_df.plot(x='公告日期', y='资产负债率', ax=ax2, color=color_list[0], linestyle='--', legend=False)
    analysis_df.plot(x='公告日期', y='资产负债率（不含预收款）', ax=ax2, color=color_list[1], linestyle='--', legend=False)

    # 绘制流动比率和速动比率的折线图
    analysis_df.plot(x='公告日期', y='流动比率', ax=ax1, color=color_list[2], linestyle='-', legend=False)
    analysis_df.plot(x='公告日期', y='速动比率', ax=ax1, color=color_list[3], linestyle='-', legend=False)

    # 设置左右两侧y轴的标签，图标题
    ax1.set_title(stock_name + '偿债能力')
    ax1.set_ylabel('流动比率/速动比率', fontsize=12)
    ax2.set_ylabel('资产负债率', fontsize=12)

    # 设置左侧y轴百分比格式
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

    # 添加图例
    ax1.legend(['流动比率', '速动比率'], loc='upper left')
    ax2.legend(['资产负债率', '资产负债率（不含预收款）'], loc='upper right')
    ax1.grid(False)
    ax2.grid(False)

    # 3.盈利能力
    # 盈利能力
    fig3, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # 绘制净利润、毛利润、营业收入柱状图
    analysis_df.plot(x='公告日期', y='净利润', kind='bar', ax=ax1, color=color_list[0], legend=False)
    analysis_df.plot(x='公告日期', y='毛利润', kind='bar', ax=ax1, color=color_list[1], legend=False,
                     bottom=analysis_df['净利润'])
    analysis_df.plot(x='公告日期', y='营业收入', kind='bar', ax=ax1, color=color_list[2], legend=False,
                     bottom=analysis_df['净利润'] + analysis_df['毛利润'])

    # 绘制毛利率和净利率折线图
    analysis_df.plot(x='公告日期', y='毛利率', ax=ax2, color=color_list[3], linestyle='--', legend=False)
    analysis_df.plot(x='公告日期', y='净利率', ax=ax2, color=color_list[0], linestyle='--', legend=False)

    # 设置左右两侧y轴的标签，图标题
    ax1.set_title(stock_name + '盈利能力')
    ax1.set_ylabel('净利润/毛利润/营业收入', fontsize=12)
    ax2.set_ylabel('毛利率/净利率', fontsize=12)

    # 设置左侧y轴的数值格式
    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))

    # 添加图例
    ax1.legend(['净利润', '毛利润', '营业收入'], loc='upper left')
    ax2.legend(['毛利率', '净利率'], loc='upper right')

    # 设置x轴标签旋转角度
    plt.xticks(rotation=45)

    # 4.现金流量趋势
    # 取出现金流量数据
    cash_flow = analysis_df[['公告日期', '经营活动产生的现金流量净额', '投资活动产生的现金流量净额', '筹资活动产生的现金流量净额']]
    cash_flow = cash_flow.set_index('公告日期')

    # 绘制折线图
    fig, ax = plt.subplots(figsize=(10, 6))

    cash_flow.plot(ax=ax, linewidth=2.5)

    # 设置标题和标签
    ax.set_title(f'{stock_name}现金流量趋势图', fontsize=18)
    ax.set_xlabel('日期', fontsize=14)
    ax.set_ylabel('现金流量（万元）', fontsize=14)

    # 添加图例
    ax.legend(fontsize=12)

    # 5.资产结构
    # 获取资产结构数据
    assets = ['货币资金', '应收账款', '存货', '固定资产']
    data = analysis_df.loc[:, ['公告日期'] + assets].set_index('公告日期')

    # 绘制堆积柱状图
    fig, ax = plt.subplots()
    data.plot(kind='bar', stacked=True, ax=ax)

    # 设置图表标题和坐标轴标签
    ax.set_title(f'{stock_name} 资产结构变化图')
    ax.set_xlabel('年份')
    ax.set_ylabel('金额（亿元）')

    # 添加图例
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)

    # 调整x轴刻度标签，只显示年份
    x_labels = [x[:4] for x in data.index]
    ax.set_xticklabels(x_labels)

    plt.tick_params(axis='x', labelrotation=45)

    # 行业比较
    # 计算同行业历年平均资产周转率
    industry_mean = industry_df
    industry_mean = industry_mean.groupby('公告日期')[['净资产收益率', '权益乘数', '利润率', '资产周转率']].mean()

    # 创建画布和坐标轴
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # 绘制资产周转率折线图
    axs[0, 0].plot(analysis_df['公告日期'], analysis_df['资产周转率'], color='blue', label=f'{stock_name}资产周转率')
    axs[0, 0].plot(industry_mean.index, industry_mean['资产周转率'], color='red', label=f'{industry_name}行业资产周转率')
    axs[0, 0].set_title(f"{stock_name}与{industry_name}行业平均值资产周转率对比")
    axs[0, 0].legend(loc='upper left')
    axs[0, 0].set_ylabel('资产周转率')
    x_labels = [x[:4] for x in analysis_df['公告日期']]
    axs[0, 0].set_xticks(range(len(x_labels)))
    axs[0, 0].set_xticklabels(x_labels)

    # 绘制净资产收益率折线图
    axs[0, 1].plot(analysis_df['公告日期'], analysis_df['净资产收益率'], color='blue', label=f'{stock_name}净资产收益率')
    axs[0, 1].plot(industry_mean.index, industry_mean['净资产收益率'], color='red', label=f'{industry_name}行业净资产收益率')
    axs[0, 1].set_title(f"{stock_name}与{industry_name}行业平均值净资产收益率对比")
    axs[0, 1].legend(loc='upper left')
    axs[0, 1].set_ylabel('净资产收益率')
    x_labels = [x[:4] for x in analysis_df['公告日期']]
    axs[0, 1].set_xticks(range(len(x_labels)))
    axs[0, 1].set_xticklabels(x_labels)

    # 绘制利润率折线图
    axs[1, 0].plot(analysis_df['公告日期'], analysis_df['利润率'], color='blue', label=f'{stock_name}利润率')
    axs[1, 0].plot(industry_mean.index, industry_mean['利润率'], color='red', label=f'{industry_name}行业利润率')
    axs[1, 0].set_title(f"{stock_name}与{industry_name}行业平均值利润率对比")
    axs[1, 0].legend(loc='upper left')
    axs[1, 0].set_ylabel('利润率')
    x_labels = [x[:4] for x in analysis_df['公告日期']]
    axs[1, 0].set_xticks(range(len(x_labels)))
    axs[1, 0].set_xticklabels(x_labels)

    # 绘制权益乘数折线图
    axs[1, 1].plot(analysis_df['公告日期'], analysis_df['权益乘数'], color='blue', label=f'{stock_name}权益乘数')
    axs[1, 1].plot(industry_mean.index, industry_mean['权益乘数'], color='red', label=f'{industry_name}行业权益乘数')
    axs[1, 1].set_title(f"{stock_name}与{industry_name}行业平均值权益乘数对比")
    axs[1, 1].legend(loc='upper left')
    axs[1, 1].set_ylabel('权益乘数')
    x_labels = [x[:4] for x in analysis_df['公告日期']]
    axs[1, 1].set_xticks(range(len(x_labels)))
    axs[1, 1].set_xticklabels(x_labels)

    plt.show()

    return True  # 表示数据已经可视化
