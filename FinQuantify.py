import os
from spider.spider import spider_data
from preprocess.preprocess import data_preprocessing
from visualization.visualization import visualize_data

total_df = None  # 全局变量，保存预处理后的数据

# 数据预处理函数
def preprocess_data():
    global total_df
    print("数据预处理中...")
    total_df = data_preprocessing()
    print("数据预处理成功！")

# 可视化函数
def visualize():
    global total_df
    # 输入股票代码
    while True:
        try:
            stock_code = input("请输入股票代码(格式如：600588.SH) ：")
            if stock_code in total_df['股票代码'].unique():
                break
            else:
                print("股票代码不存在，请重新输入！")
        except KeyboardInterrupt:
            print("\n程序已退出！")
            exit(0)
    # 可视化数据
    visualize_data(total_df, stock_code)
    print('数据可视化成功')

# 检查数据是否存在
def main():
    global total_df
    if os.path.exists('./data/利润表.csv') and os.path.exists('./data/现金流量表.csv') and os.path.exists('./data/资产负债表.csv'):
        print("数据已存在，不需要爬虫。")
        if total_df is None:  # 检查是否需要进行数据预处理
            preprocess_data()  # 进行数据预处理
        visualize()  # 调用可视化函数
    else:
        # 如果数据不存在，询问是否要爬取数据
        print("数据不存在，请问是否要爬取数据？")
        choice = input("请输入 Y 表示是，N 表示否：")
        if choice.lower() == "y":
            print("开始爬虫...")
            spider = spider_data()
            if spider:
                preprocess_data()  # 进行数据预处理
                visualize()  # 调用可视化函数
            else:
                print("网络错误，爬虫失败！")
                exit(1)
        else:
            print("程序运行结束，感谢使用FinQuantify！")
            exit(0)

    # 询问是否需要分析其他公司
    while True:
        try:
            choice = input("是否需要分析其他公司？请输入 Y 表示是，N 表示否：")
            if choice.lower() == "y" or choice.lower() == "n":
                break
            else:
                print("输入有误，请重新输入！")
        except KeyboardInterrupt:
            print("\n程序已退出！")
            exit(0)
    if choice.lower() == "y":
        main()
    else:
        print("程序运行结束，感谢使用FinQuantify！")


if __name__ == '__main__':
    print("欢迎使用FinQuantify！")
    main()
