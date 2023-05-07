# coding=utf-8
# 导入所需库
import os
import json
import requests
import pandas as pd

def spider_data():
    # 设置爬取页面数据量
    report_date_list = ['2011-12-31', '2012-12-31', '2013-12-31', '2014-12-31', '2015-12-31', '2016-12-31',
                        '2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31', '2022-12-31']
    pageSize = 500
    pageNumber_list = range(20)  # 不会超过20了
    print('#---爬取资产负债表---')
    # 改表头，结合网址去查看
    zcfz_name2code_dict = {
        '股票代码': 'SECUCODE'
        , '股票简称': 'SECURITY_NAME_ABBR'
        , '行业名称': 'INDUSTRY_NAME'
        , '公告日期': 'REPORT_DATE'
        , '总资产': 'TOTAL_ASSETS'
        , '固定资产': 'FIXED_ASSET'
        , '货币资金': 'MONETARYFUNDS'
        , '应收账款': 'ACCOUNTS_RECE'
        , '存货': 'INVENTORY'
        , '总负债': 'TOTAL_LIABILITIES'
        , '应付账款': 'ACCOUNTS_PAYABLE'
        , '预收账款': 'ADVANCE_RECEIVABLES'
        , '所有者权益': 'TOTAL_EQUITY'
    }
    zcfz_code2name_dict = {v: k for k, v in zcfz_name2code_dict.items()}


    # --------------------------------------------------------------------------------
    # 开始爬虫
    def get_zcfz_df_v2(api, code2name_dict):
        while True:
            try:
                res = json.loads(requests.get(api).text)['result']
                if res == None:  # 如果为空就不解析了
                    return pd.DataFrame([])
                zcfz_df = pd.DataFrame(res['data'])
                zcfz_df = zcfz_df.loc[:, list(code2name_dict.keys())]
                zcfz_df = zcfz_df.rename(columns=code2name_dict)
                return zcfz_df
            except requests.exceptions.RequestException as e:
                print("网络异常或其他异常，请检查程序运行环境")
                while True:
                    choice = input("是否要重新执行爬虫？(Y/N) ")
                    if choice.upper() == "Y":
                        break
                    elif choice.upper() == "N":
                        return False  # 表示用户选择退出程序
                    else:
                        print("无效的输入，请重新输入")


    total_zcfz_df = pd.DataFrame([])
    for REPORT_DATE in report_date_list:
        print('开始获取', REPORT_DATE)
        for pageNumber in pageNumber_list:
            zcfz_api = f'https://datacenter-web.eastmoney.com/api/data/v1/get?&sortColumns=NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&' \
                       f'pageSize={pageSize}&pageNumber={pageNumber}&reportName=RPT_DMSK_FN_BALANCE&columns=ALL&filter=(SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)' \
                       f'(REPORT_DATE%3D%27{REPORT_DATE}%27)'
            tmp_zcfz_df = get_zcfz_df_v2(zcfz_api, code2name_dict=zcfz_code2name_dict)
            if tmp_zcfz_df.shape[0] == 0:
                break
            else:
                if total_zcfz_df.shape[0] == 0:
                    total_zcfz_df = tmp_zcfz_df
                else:
                    total_zcfz_df = pd.concat([total_zcfz_df, tmp_zcfz_df], axis=0)
    print('#---爬取利润表---')
    # 爬取现金流量表
    # 改表头，结合网址去查看
    lrb_name2code_dict = {
        '股票代码': 'SECUCODE'
        , '股票简称': 'SECURITY_NAME_ABBR'
        , '行业名称': 'INDUSTRY_NAME'
        , '公告日期': 'REPORT_DATE'
        , '营业收入': 'TOTAL_OPERATE_INCOME'
        , '营业成本': 'OPERATE_COST'
        , '销售费用': 'SALE_EXPENSE'
        , '管理费用': 'MANAGE_EXPENSE'
        , '财务费用': 'FINANCE_EXPENSE'
        , '营业总支出': 'TOTAL_OPERATE_COST'
        , '营业利润': 'OPERATE_PROFIT'
        , '利润总额': 'TOTAL_PROFIT'
        , '所得税费用': 'INCOME_TAX'
        , '净利润': 'PARENT_NETPROFIT'
    }
    lrb_code2name_dict = {v: k for k, v in lrb_name2code_dict.items()}


    # 开始爬虫
    def get_lrb_df_v2(api, code2name_dict):
        while True:
            try:
                res = json.loads(requests.get(api).text)['result']
                if res == None:  # 如果为空就不解析了
                    return pd.DataFrame([])
                lrb_df = pd.DataFrame(res['data'])
                lrb_df = lrb_df.loc[:, list(code2name_dict.keys())]
                lrb_df = lrb_df.rename(columns=code2name_dict)
                return lrb_df
            except requests.exceptions.RequestException as e:
                print("网络异常或其他异常，请检查程序运行环境")
                while True:
                    choice = input("是否要重新执行爬虫？(Y/N) ")
                    if choice.upper() == "Y":
                        break
                    elif choice.upper() == "N":
                        return False  # 表示用户选择退出程序
                    else:
                        print("无效的输入，请重新输入")


    total_lrb_df = pd.DataFrame([])
    for REPORT_DATE in report_date_list:
        print('开始获取', REPORT_DATE)
        for pageNumber in pageNumber_list:
            lrb_api = f'https://datacenter-web.eastmoney.com/api/data/v1/get?&sortColumns=NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&' \
                      f'pageSize={pageSize}&pageNumber={pageNumber}&reportName=RPT_DMSK_FN_INCOME&columns=ALL&filter=(SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)' \
                      f'(REPORT_DATE%3D%27{REPORT_DATE}%27)'
            tmp_lrb_df = get_lrb_df_v2(lrb_api, code2name_dict=lrb_code2name_dict)
            if tmp_lrb_df.shape[0] == 0:
                break
            else:
                if tmp_lrb_df.shape[0] == 0:
                    total_lrb_df = tmp_lrb_df
                else:
                    total_lrb_df = pd.concat([total_lrb_df, tmp_lrb_df], axis=0)

    print('#---爬取现金流量表---')
    # 爬取现金流量表
    # 改表头，结合网址去查看
    xjll_name2code_dict = {
        '股票代码': 'SECUCODE',
        '股票简称': 'SECURITY_NAME_ABBR',
        '行业名称': 'INDUSTRY_NAME',
        '公告日期': 'REPORT_DATE',
        '净现金流(元)': 'NETCASH_OPERATE',
        '经营活动产生的现金流量净额': 'NETCASH_OPERATE',
        '投资活动产生的现金流量净额': 'NETCASH_INVEST',
        '筹资活动产生的现金流量净额': 'NETCASH_FINANCE'
    }

    xjll_code2name_dict = {v: k for k, v in xjll_name2code_dict.items()}


    # 开始爬虫
    def get_xjll_df_v2(api, code2name_dict):
        while True:
            try:
                res = json.loads(requests.get(api).text)['result']
                if res == None:  # 如果为空就不解析了
                    return pd.DataFrame([])
                xjll_df = pd.DataFrame(res['data'])
                xjll_df = xjll_df.loc[:, list(code2name_dict.keys())]
                xjll_df = xjll_df.rename(columns=code2name_dict)
                return xjll_df
            except requests.exceptions.RequestException as e:
                print("网络异常或其他异常，请检查程序运行环境")
                while True:
                    choice = input("是否要重新执行爬虫？(Y/N) ")
                    if choice.upper() == "Y":
                        break
                    elif choice.upper() == "N":
                        return False  # 表示用户选择退出程序
                    else:
                        print("无效的输入，请重新输入")


    total_xjll_df = pd.DataFrame([])
    for REPORT_DATE in report_date_list:
        print('开始获取', REPORT_DATE)
        for pageNumber in pageNumber_list:
            xjll_api = f'https://datacenter-web.eastmoney.com/api/data/v1/get?&sortColumns=NOTICE_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&' \
                       f'pageSize={pageSize}&pageNumber={pageNumber}&reportName=RPT_DMSK_FN_CASHFLOW&columns=ALL&filter=(SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)' \
                       f'(REPORT_DATE%3D%27{REPORT_DATE}%27)'
            tmp_xjll_df = get_xjll_df_v2(xjll_api, code2name_dict=xjll_code2name_dict)
            if tmp_xjll_df.shape[0] == 0:
                break
            else:
                if tmp_xjll_df.shape[0] == 0:
                    total_xjll_df = tmp_xjll_df
                else:
                    total_xjll_df = pd.concat([total_xjll_df, tmp_xjll_df], axis=0)

    # 创建保存数据的文件夹
    if not os.path.exists('data'):
        os.makedirs('data')

    print('#---保存---')
    # 将 DataFrame 保存到 csv文件
    total_zcfz_df.to_csv(f'./data/资产负债表.csv', index=False)
    total_lrb_df.to_csv(f'./data/利润表.csv', index=False)
    total_xjll_df.to_csv(f'./data/现金流量表.csv', index=False)
    print('已保存，爬虫结束 ！')

    return True  # 表示数据已经成功爬取并保存